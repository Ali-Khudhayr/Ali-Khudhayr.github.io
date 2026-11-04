import {traceDrawing} from './trace.mjs';
self.onmessage=event=>{
  const {pixels,width,height,style}=event.data;
  try{self.postMessage({result:traceDrawing(pixels,width,height,style)});}
  catch(error){self.postMessage({error:error.message});}
};
