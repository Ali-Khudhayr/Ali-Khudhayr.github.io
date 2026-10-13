const React=require('react');const RDS=require('react-dom/server');const sharp=require('sharp');
const lu=require('react-icons/lu');
const want={std_controls:'LuSlidersHorizontal',std_meter:'LuGauge',std_wiring:'LuCable',std_lv:'LuShieldCheck'};
(async()=>{for(const [n,k] of Object.entries(want)){
 if(!lu[k]){console.log('missing',k);continue}
 const svg=RDS.renderToStaticMarkup(React.createElement(lu[k],{size:256,color:'#FFFFFF',strokeWidth:2}));
 await sharp(Buffer.from(svg)).resize(256,256).png().toFile(n+'.png');console.log(n)}})();
