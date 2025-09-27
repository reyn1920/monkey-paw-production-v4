const TinyChart=(function(){function line(ctx,arr,opt){opt=opt||{}; const w=ctx.canvas.width,h=ctx.canvas.height;
const pad=30; const max=Math.max(...arr,1), min=Math.min(...arr,0);
ctx.strokeStyle=opt.color||"#999"; ctx.lineWidth=2; ctx.beginPath();
arr.forEach((v,i)=>{const x=pad+(w-2*pad)*(i/(arr.length-1||1)); const y=h-pad-(h-2*pad)*((v-min)/(max-min||1));
if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);}); ctx.stroke();
ctx.fillStyle="#aaa"; ctx.font="12px sans-serif"; ctx.fillText(opt.label||"", pad, 14);} return {line};})();