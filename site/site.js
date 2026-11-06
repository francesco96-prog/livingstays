(function(){
var d=document,h=d.documentElement,intro=d.querySelector('.intro');
if(intro&&!h.classList.contains('seen')){try{sessionStorage.setItem('ls-intro','1')}catch(e){}
setTimeout(function(){intro.classList.add('out')},1500);}
var hd=d.querySelector('.hd');
d.querySelector('.bur').onclick=function(){hd.classList.toggle('open')};
var sc=function(){hd.classList.toggle('sc',scrollY>10)};addEventListener('scroll',sc,{passive:true});sc();
d.addEventListener('click',function(e){var l=d.querySelector('.lang[open]');if(l&&!l.contains(e.target))l.removeAttribute('open')});
var rv=d.querySelectorAll('.rv');
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(x){io.observe(x)})}else rv.forEach(function(x){x.classList.add('in')});
/* lightbox */
var lb=d.querySelector('.lb');
if(lb){var im=lb.querySelector('img'),set=[],i=0;
var show=function(){im.src=set[i]};
d.querySelectorAll('.gal').forEach(function(g){var bs=[].slice.call(g.querySelectorAll('button'));
bs.forEach(function(b,k){b.onclick=function(){set=bs.map(function(x){return x.querySelector('img').src});i=k;show();lb.classList.add('on')}})});
lb.querySelector('.x').onclick=function(){lb.classList.remove('on')};
lb.querySelector('.p').onclick=function(){i=(i-1+set.length)%set.length;show()};
lb.querySelector('.n').onclick=function(){i=(i+1)%set.length;show()};
lb.onclick=function(e){if(e.target===lb)lb.classList.remove('on')};
d.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;if(e.key=='Escape')lb.classList.remove('on');if(e.key=='ArrowLeft')lb.querySelector('.p').click();if(e.key=='ArrowRight')lb.querySelector('.n').click()});}
/* mail forms */
d.querySelectorAll('form[data-to]').forEach(function(f){f.onsubmit=function(e){e.preventDefault();
var b=[];[].forEach.call(f.elements,function(x){if(x.name&&x.value)b.push(x.getAttribute('data-l')+': '+x.value)});
location.href='mailto:'+f.getAttribute('data-to')+'?subject='+encodeURIComponent(f.getAttribute('data-s'))+'&body='+encodeURIComponent(b.join('\n'))}});
})();
