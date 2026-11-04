// Gaussian smoothing, non-maximum suppression and hysteresis keep detailed photos readable as ink.
export function traceLegacyContours(rgba,width,height,settings={}){
  const size=width*height,gray=new Float32Array(size),blurX=new Float32Array(size),smooth=new Float32Array(size),magnitude=new Float32Array(size),direction=new Uint8Array(size),thin=new Float32Array(size);
  for(let i=0;i<size;i++)gray[i]=rgba[i*4]*.299+rgba[i*4+1]*.587+rgba[i*4+2]*.114;
  const kernel=[1,4,6,4,1];
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){let sum=0;for(let k=-2;k<=2;k++)sum+=gray[y*width+Math.max(0,Math.min(width-1,x+k))]*kernel[k+2];blurX[y*width+x]=sum/16;}
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){let sum=0;for(let k=-2;k<=2;k++)sum+=blurX[Math.max(0,Math.min(height-1,y+k))*width+x]*kernel[k+2];smooth[y*width+x]=sum/16;}
  for(let y=1;y<height-1;y++)for(let x=1;x<width-1;x++){
    const i=y*width+x,gx=-smooth[i-width-1]+smooth[i-width+1]-2*smooth[i-1]+2*smooth[i+1]-smooth[i+width-1]+smooth[i+width+1],gy=-smooth[i-width-1]-2*smooth[i-width]-smooth[i-width+1]+smooth[i+width-1]+2*smooth[i+width]+smooth[i+width+1];
    magnitude[i]=Math.hypot(gx,gy);let angle=Math.atan2(gy,gx)*180/Math.PI;if(angle<0)angle+=180;direction[i]=angle<22.5||angle>=157.5?0:angle<67.5?1:angle<112.5?2:3;
  }
  const strengths=[];
  for(let y=2;y<height-2;y++)for(let x=2;x<width-2;x++){
    const i=y*width+x,offset=[1,width+1,width,width-1][direction[i]],v=magnitude[i];
    if(v>=magnitude[i-offset]&&v>=magnitude[i+offset]&&v>(settings.floor??12)){thin[i]=v;strengths.push(v);}
  }
  strengths.sort((a,b)=>a-b);const high=Math.max(settings.minimum??28,Math.min(155,strengths[Math.floor(strengths.length*(settings.quantile??.76))]||55)),low=high*.38;
  const edges=new Uint8Array(size),stack=[];
  for(let i=0;i<size;i++)if(thin[i]>=high){edges[i]=1;stack.push(i);}
  const offsets=[-width-1,-width,-width+1,-1,1,width-1,width,width+1];
  while(stack.length){const i=stack.pop();for(const offset of offsets){const next=i+offset;if(next<0||next>=size||Math.abs(next%width-i%width)>1||edges[next]||thin[next]<low)continue;edges[next]=1;stack.push(next);}}
  const used=new Uint8Array(size),paths=[];
  const neighbours=i=>{const y=Math.floor(i/width),x=i%width;return offsets.map(o=>i+o).filter(n=>n>=0&&n<size&&Math.abs(n%width-x)<=1&&Math.abs(Math.floor(n/width)-y)<=1&&edges[n]&&!used[n]);};
  function follow(start){
    let index=start,previous=-1,points=[],strength=0;
    for(let count=0;count<1200;count++){
      used[index]=1;points.push([index%width,Math.floor(index/width)]);strength+=magnitude[index];const options=neighbours(index);if(!options.length)break;
      const x=index%width,y=Math.floor(index/width),px=previous<0?x:previous%width,py=previous<0?y:Math.floor(previous/width);
      options.sort((a,b)=>{const score=n=>{const dx=n%width-x,dy=Math.floor(n/width)-y,alignment=previous<0?0:((x-px)*dx+(y-py)*dy)/Math.hypot(dx,dy);return alignment*30+magnitude[n]*.06;};return score(b)-score(a);});
      previous=index;index=options[0];
    }
    if(points.length<(settings.minPoints??9))return;
    // Remove redundant points while retaining the contour's bends.
    const simplified=[points[0]];
    for(let i=1;i<points.length-1;i++){const a=points[i-1],b=points[i],c=points[i+1];if((b[0]-a[0])*(c[1]-b[1])!==(b[1]-a[1])*(c[0]-b[0])||i%5===0)simplified.push(b);}
    simplified.push(points.at(-1));let length=0;for(let i=1;i<points.length;i++)length+=Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]);
    paths.push({points:simplified.map(([x,y])=>[x/width,y/height]),weight:Math.max(3,Math.min(length,100)),width:.00105,strength:strength/points.length,length});
  }
  // Start at contour endpoints, then trace closed loops and branches.
  for(let i=0;i<size;i++)if(edges[i]&&!used[i]&&neighbours(i).length===1)follow(i);
  for(let i=0;i<size;i++)if(edges[i]&&!used[i])follow(i);
  paths.sort((a,b)=>(b.length*Math.sqrt(b.strength))-(a.length*Math.sqrt(a.strength)));
  const selected=paths.slice(0,settings.limit??650);
  // Alternate salient contours with finer detail, without breaking individual pen strokes.
  const ordered=[];for(let i=0;i<selected.length;i+=3){ordered.push(selected[i]);if(selected[i+2])ordered.push(selected[i+2]);if(selected[i+1])ordered.push(selected[i+1]);}
  return ordered;
}

export const TRACE_VERSION=2;
// Analysis resolution follows source detail, with a fixed upper bound for local devices.
export function analysisSize(width,height,style='balanced'){
  const max=style==='legacy'?[560,460]:style==='detail'?[1100,850]:[860,680];
  const ratio=Math.min(max[0]/width,max[1]/height,1);
  return {width:Math.max(3,Math.round(width*ratio)),height:Math.max(3,Math.round(height*ratio))};
}

// Ramer–Douglas–Peucker in pixel coordinates; endpoints and closed-loop geometry survive.
export function simplifyContour(points,tolerance=.75){
  if(points.length<=2)return points.slice();
  const keep=new Uint8Array(points.length);keep[0]=keep[points.length-1]=1;
  const stack=[[0,points.length-1]],limit=tolerance*tolerance;
  while(stack.length){const [a,b]=stack.pop(),[ax,ay]=points[a],[bx,by]=points[b],dx=bx-ax,dy=by-ay,len=dx*dx+dy*dy;let far=limit,index=-1;
    for(let i=a+1;i<b;i++){const [x,y]=points[i],t=len?Math.max(0,Math.min(1,((x-ax)*dx+(y-ay)*dy)/len)):0,d=(x-ax-t*dx)**2+(y-ay-t*dy)**2;if(d>far){far=d;index=i;}}
    if(index>=0){keep[index]=1;stack.push([a,index],[index,b]);}
  }
  return points.filter((_,i)=>keep[i]);
}
function geometry(path,width,height){
  const points=path.points;let length=0;for(let i=1;i<points.length;i++)length+=Math.hypot((points[i][0]-points[i-1][0])*width,(points[i][1]-points[i-1][1])*height);
  return {...path,length,weight:Math.max(2,Math.min(160,length)),points};
}

// Only bridge a short, aligned gap. Do not join unrelated nearby parallel edges.
export function bridgeContours(paths,width,height,maxGap=3){
  const result=paths.map(p=>({...p,points:p.points.map(p=>p.slice())})),used=new Set();
  const distance=(a,b)=>Math.hypot((a[0]-b[0])*width,(a[1]-b[1])*height);
  for(let i=0;i<result.length;i++){
    if(used.has(i))continue;const p=result[i];
    for(let pass=0;pass<2;pass++){
      if(pass)p.points.reverse();const end=p.points.at(-1),prev=p.points.at(-2);let best=null;
      for(let j=i+1;j<result.length;j++){
        if(used.has(j)||result[j].level!==p.level)continue;const q=result[j];
        for(const reverse of [false,true]){const next=reverse?q.points.at(-1):q.points[0],after=reverse?q.points.at(-2):q.points[1],gap=distance(end,next);if(gap>.05&&gap<=maxGap){
          const dot=(a,b)=>a[0]*b[0]+a[1]*b[1],unit=(a,b)=>{const dx=(b[0]-a[0])*width,dy=(b[1]-a[1])*height,n=Math.hypot(dx,dy)||1;return [dx/n,dy/n];};
          if(dot(unit(prev,end),unit(end,next))>.72&&dot(unit(end,next),unit(next,after))>.72&&(!best||gap<best.gap))best={j,reverse,gap};
        }}
      }
      if(best){const q=result[best.j];p.points.push(...(best.reverse?q.points.toReversed():q.points));used.add(best.j);p.strength=(p.strength+q.strength)/2;}
    }
    p.points.reverse();
  }
  return result.filter((_,i)=>!used.has(i)).map(p=>geometry(p,width,height));
}

export function traceDrawing(rgba,width,height,style='balanced'){
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<3||height<3||width*height>1_000_000||rgba?.length!==width*height*4)throw new Error('بيانات تحليل الصورة غير صالحة.');
  if(style==='legacy'){const paths=traceLegacyContours(rgba,width,height);return {paths,version:TRACE_VERSION,mode:'legacy',fallback:null,levels:{general:0,medium:paths.length,fine:0}};}
  const detail=style==='detail',faint=style==='faint',cw=Math.max(3,Math.floor(width/2)),ch=Math.max(3,Math.floor(height/2)),coarse=new Uint8ClampedArray(cw*ch*4);
  for(let y=0;y<ch;y++)for(let x=0;x<cw;x++)for(let c=0;c<4;c++){let total=0;for(let dy=0;dy<2;dy++)for(let dx=0;dx<2;dx++)total+=rgba[(Math.min(height-1,y*2+dy)*width+Math.min(width-1,x*2+dx))*4+c];coarse[(y*cw+x)*4+c]=total/4;}
  const settings=faint?{floor:8,minimum:18,quantile:.7,minPoints:7,limit:1400}:{limit:1400,minPoints:7};
  const general=traceLegacyContours(coarse,cw,ch,settings).filter(p=>p.length>Math.max(10,Math.hypot(cw,ch)*.025)).map(p=>({...p,level:'general'}));
  const full=traceLegacyContours(rgba,width,height,settings);
  const mask=new Uint8Array(width*height);
  for(const path of general)for(let i=1;i<path.points.length;i++){
    const a=path.points[i-1],b=path.points[i],steps=Math.max(1,Math.ceil(Math.hypot((b[0]-a[0])*width,(b[1]-a[1])*height)));
    for(let s=0;s<=steps;s++){const x=Math.round((a[0]+(b[0]-a[0])*s/steps)*width),y=Math.round((a[1]+(b[1]-a[1])*s/steps)*height);for(let dy=-3;dy<=3;dy++)for(let dx=-3;dx<=3;dx++)if(x+dx>=0&&x+dx<width&&y+dy>=0&&y+dy<height)mask[(y+dy)*width+x+dx]=1;}
  }
  const remaining=full.filter(p=>{
    let covered=0,total=0;for(let i=1;i<p.points.length;i++){const a=p.points[i-1],b=p.points[i],steps=Math.max(1,Math.ceil(Math.hypot((b[0]-a[0])*width,(b[1]-a[1])*height)/2));for(let s=0;s<=steps;s++){const x=Math.min(width-1,Math.max(0,Math.round((a[0]+(b[0]-a[0])*s/steps)*width))),y=Math.min(height-1,Math.max(0,Math.round((a[1]+(b[1]-a[1])*s/steps)*height)));total++;covered+=mask[y*width+x];}}
    return covered/Math.max(1,total)<.72;
  }).map(p=>({...p,level:p.length>Math.hypot(width,height)*.05?'medium':'fine'}));
  let paths=[...general,...remaining].map(p=>geometry({...p,points:simplifyContour(p.points.map(([x,y])=>[x*width,y*height]),p.level==='general'?1.05:.65).map(([x,y])=>[x/width,y/height])},width,height));
  paths=bridgeContours(paths,width,height);
  const rank={general:0,medium:1,fine:2};
  paths.sort((a,b)=>rank[a.level]-rank[b.level]||b.length*Math.sqrt(b.strength)-a.length*Math.sqrt(a.strength));
  // Reserve a bounded detail budget, instead of allowing texture to consume the whole drawing.
  const limits=detail?{general:280,medium:260,fine:440}:{general:240,medium:220,fine:220},counts={general:0,medium:0,fine:0};
  paths=paths.filter(p=>++counts[p.level]<=limits[p.level]).map(p=>({...p,width:p.level==='general'?.00165:p.level==='medium'?.0012:.00085}));
  let fallback=null;
  if(paths.length<3&&full.length>=3){paths=full.map(p=>({...p,level:'medium'}));fallback='sparse-use-original';}
  const levels={general:0,medium:0,fine:0};for(const p of paths)levels[p.level]++;
  return {paths,version:TRACE_VERSION,mode:style,fallback,levels,weak:paths.length<5};
}
export function traceContours(rgba,width,height){return traceDrawing(rgba,width,height).paths;}
