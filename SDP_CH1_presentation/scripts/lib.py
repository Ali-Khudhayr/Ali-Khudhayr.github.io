import re, uuid
EMU=914400
def E(v): return int(round(v*EMU))
NS='xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
INK,SLATE,AMBER,CARD,TEAL,RED='0E1B2C','5B6B7F','B45309','F1F5F9','0F766E','DC2626'
STYLE='<p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style>'
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def xfrm(x,y,w,h): return f'<a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
def run(t,sz,col=INK,font='Segoe UI Semibold',i=0,spc=None):
    sp=f' spc="{spc}"' if spc else ''
    pre=' xml:space="preserve"' if t!=t.strip() else ''
    return f'<a:r><a:rPr lang="en-US" sz="{int(sz*100)}" b="0" i="{i}"{sp} dirty="0"><a:solidFill><a:srgbClr val="{col}"/></a:solidFill><a:latin typeface="{font}"/></a:rPr><a:t{pre}>{esc(t)}</a:t></a:r>'
def para(runs,algn='l',after=0,lnpct=None):
    ln=f'<a:lnSpc><a:spcPct val="{lnpct}"/></a:lnSpc>' if lnpct else ''
    af=f'<a:spcAft><a:spcPts val="{after}"/></a:spcAft>' if after else ''
    inner=ln+af
    ppr=f'<a:pPr algn="{algn}">{inner}</a:pPr>' if inner else f'<a:pPr algn="{algn}"/>'
    return f'<a:p>{ppr}{"".join(runs)}</a:p>'
def text(id,name,x,y,w,h,paras,anchor='t',autofit=True):
    fit='<a:spAutoFit/>' if autofit else '<a:noAutofit/>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h)}'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}">{fit}</a:bodyPr><a:lstStyle/>{"".join(paras)}</p:txBody></p:sp>')
def shape(id,name,x,y,w,h,fill,prst='roundRect',adj=6666,alpha=None):
    av=f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if prst=='roundRect' else '<a:avLst/>'
    al=f'<a:alpha val="{alpha}"/>' if alpha else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="{prst}">{av}</a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}">{al}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln><a:effectLst/></p:spPr>{STYLE}<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')
def flat(id,name,x,y,w,h,fill,prst='rect',alpha=None):
    al=f'<a:alpha val="{alpha}"/>' if alpha else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}">{al}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')
def pic(id,name,rid,x,y,w,h,descr=''):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{id}" name="{name}" descr="{esc(descr)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
def video(id,name,rid_media,rid_video,rid_poster,x,y,w,h,descr=''):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{id}" name="{name}" descr="{esc(descr)}"><a:hlinkClick r:id="" action="ppaction://media"/></p:cNvPr><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr><a:videoFile r:link="{rid_video}"/><p:extLst><p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}"><p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" r:embed="{rid_media}"/></p:ext></p:extLst></p:nvPr></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid_poster}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
def group(id,name,x,y,w,h,children):
    return (f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="{id}" name="{name}"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/>'
            f'<a:chOff x="{E(x)}" y="{E(y)}"/><a:chExt cx="{E(w)}" cy="{E(h)}"/></a:xfrm></p:grpSpPr>{"".join(children)}</p:grpSp>')
def pageno(id,n):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="pageno"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(11.58,7.0,1.0,0.3)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="r"/>{slidenum_fld(n)}</a:p></p:txBody></p:sp>')
def slidenum_fld(n,sz=1100):
    return (f'<a:fld id="{{{str(uuid.uuid4()).upper()}}}" type="slidenum"><a:rPr lang="en-US" sz="{sz}" b="0" i="0"><a:solidFill><a:srgbClr val="{SLATE}"/></a:solidFill><a:latin typeface="Bahnschrift"/></a:rPr><a:t>{n}</a:t></a:fld>')
def header(kicker,title,n,ids=(2,3,4,5)):
    return [text(ids[0],'footer',0.75,7.0,7.0,0.3,[para([run('EE499  ·  Team 16  ·  Smart Home Energy Management',11,SLATE,'Segoe UI')])]),
            pageno(ids[1],n),
            text(ids[2],'kicker',0.75,0.48,11.8,0.35,[para([run(kicker,15,AMBER,spc=250)])]),
            text(ids[3],'title',0.75,0.82,11.8,0.9,[para([run(title,40,INK,'Bahnschrift SemiBold')])])]
def slide(children,timing='',bg='FFFFFF',transition=True):
    tr=('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">'
        '<mc:Choice Requires="p14"><p:transition spd="med" p14:dur="600"><p:fade/></p:transition></mc:Choice><mc:Fallback xmlns=""><p:transition spd="med"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>') if transition else ''
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:sld {NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{"".join(children)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>{tr}{timing}</p:sld>')
REL_LAYOUT='http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout'
REL_NOTES='http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide'
REL_IMG='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
REL_VID='http://schemas.openxmlformats.org/officeDocument/2006/relationships/video'
REL_MEDIA='http://schemas.microsoft.com/office/2007/relationships/media'
def rels(items):
    body=''.join(f'<Relationship Id="{i}" Type="{t}" Target="{g}"/>' for i,t,g in items)
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>'
# ---------------- timing ----------------
class T:
    def __init__(s): s.n=2
    def id(s): s.n+=1; return s.n
def fadeup(t,spid,delay):
    a,b,c,d,e=t.id(),t.id(),t.id(),t.id(),t.id(); f=t.id()
    return (f'<p:par><p:cTn id="{a}" fill="hold"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{b}" presetID="42" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
      f'<p:set><p:cBhvr><p:cTn id="{c}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
      f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{d}" dur="450"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
      f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{e}" dur="450" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="#ppt_x"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="#ppt_x"/></p:val></p:tav></p:tavLst></p:anim>'
      f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{f}" dur="450" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_y</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="#ppt_y+.1"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="#ppt_y"/></p:val></p:tav></p:tavLst></p:anim>'
      '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
def play(t,spid,delay,dur_ms):
    a,b,c=t.id(),t.id(),t.id()
    return (f'<p:par><p:cTn id="{a}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{b}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="withEffect"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>'
            f'<p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{c}" dur="{dur_ms}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
def timing(steps_fn,videos=()):
    """steps_fn(t) -> list of <p:par> step xml (auto-start chain); videos: [(spid,loop,mute)]"""
    t=T(); steps=steps_fn(t)
    main=(f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>{"".join(steps)}</p:childTnLst></p:cTn></p:par>')
    t.n=max(t.n,3)
    vids=''
    for spid,loop,mute in videos:
        i=t.id(); rc=' repeatCount="indefinite"' if loop else ''
        mu=' mute="1"' if mute else ''
        vids+=(f'<p:video><p:cMediaNode vol="80000"{mu}><p:cTn id="{i}"{rc} fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>')
    return (f'<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{main}</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            f'{vids}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
def fade_chain(spids,start=150,gap=180):
    return lambda t:[fadeup(t,s,start+i*gap) for i,s in enumerate(spids)]
