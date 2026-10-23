const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('.nav');
if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});}

document.querySelectorAll('[data-carousel]').forEach((carousel)=>{
  const track=carousel.querySelector('[data-carousel-track]');
  const slides=Array.from(track.children);
  const prev=carousel.querySelector('[data-carousel-prev]');
  const next=carousel.querySelector('[data-carousel-next]');
  const current=carousel.querySelector('[data-carousel-current]');
  const dots=Array.from(carousel.querySelectorAll('[data-carousel-dot]'));
  let active=0;

  const setActive=(index)=>{
    active=Math.max(0,Math.min(index,slides.length-1));
    current.textContent=String(active+1).padStart(2,'0');
    prev.disabled=active===0;
    next.disabled=active===slides.length-1;
    dots.forEach((dot,i)=>dot.setAttribute('aria-current',String(i===active)));
  };
  const goTo=(index)=>{
    const target=Math.max(0,Math.min(index,slides.length-1));
    track.scrollTo({left:slides[target].offsetLeft-track.offsetLeft,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    setActive(target);
  };
  prev.addEventListener('click',()=>goTo(active-1));
  next.addEventListener('click',()=>goTo(active+1));
  dots.forEach((dot)=>dot.addEventListener('click',()=>goTo(Number(dot.dataset.carouselDot))));

  let scrollTimer;
  track.addEventListener('scroll',()=>{
    window.clearTimeout(scrollTimer);
    scrollTimer=window.setTimeout(()=>{
      const closest=slides.reduce((best,slide,index)=>Math.abs(slide.offsetLeft-track.offsetLeft-track.scrollLeft)<Math.abs(slides[best].offsetLeft-track.offsetLeft-track.scrollLeft)?index:best,0);
      setActive(closest);
    },80);
  },{passive:true});
  track.addEventListener('keydown',(event)=>{
    if(event.key==='ArrowRight'){event.preventDefault();goTo(active+1);}
    if(event.key==='ArrowLeft'){event.preventDefault();goTo(active-1);}
  });
  setActive(0);
});
