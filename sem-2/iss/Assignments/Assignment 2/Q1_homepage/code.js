const size1=document.getElementById("s1");
const size2=document.getElementById("s2");
const size3=document.getElementById("s3");

const table1 = document.getElementById("skilltable1");
function myFunction(num) {
    if(num==0)
    table1.style.fontSize = "15px";
    else if(num==1)
    table1.style.fontSize = "30px";
    else
    table1.style.fontSize = "45px";
  }
// size1.addEventListener("click",function onClick(e){
//     myFunction();
// });

size1.addEventListener("click",function onClick(e){
    myFunction(0);
});
size2.addEventListener("click",function onClick(e){
    myFunction(1);
});
size3.addEventListener("click",function onClick(e){
    myFunction(2);
});

var backcount=0;
const readback=document.getElementById("readback");
const back=document.body;
function backFunction(){
    console.log('hi');
    backcount=(backcount+1)%5;
    if(backcount==1)
        back.style.backgroundImage="url('./media/bs1.gif')";
    else if(backcount==0)
    back.style.backgroundImage="url('./media/bs0.gif')";
    else if(backcount==2)
    back.style.backgroundImage="url('./media/bs2.gif')";
    else if(backcount==3)
    back.style.backgroundImage="url('./media/bs3.gif')";
    else
    back.style.backgroundImage="url('./media/bs4.gif')";
    // back.style.backgroundImage=`url('../media/bs${backcount}.gif')`;
    // console.log(`url('../media/bs${backcount}.gif')`);
}



const newslist=document.getElementById("newslist");
const newsform=document.getElementById("newsform");
let lc;

if(window.localStorage.getItem('lc')===null){
    lc=0;
}
else{
    lc=Number(window.localStorage.getItem('lc'));
    
    for(let i=1;i<=lc;i++)
    {
        // const newsinput=newsform.elements.newsinput;
        const newsval=window.localStorage.getItem(i);
        const listele=document.createElement("li");
        listele.append(newsval);
        newslist.append(listele);
    }
}
newsform.addEventListener("submit",function(e){
    e.preventDefault();
    const newsinput=newsform.elements.newsinput;
    const newsval=newsinput.value;
    if(newsval!="")
    {
        const listele=document.createElement("li");
        listele.append(newsval);
        newslist.append(listele);    

        lc++;
        window.localStorage.setItem(lc,newsval);
        window.localStorage.setItem('lc',lc);
        newsinput.value='';
    }
})

newsform.addEventListener("reset",function(e){
    e.preventDefault();
    for(let i=1;i<=lc;i++)
    {
        newslist.removeChild(newslist.firstElementChild);
        localStorage.removeItem(String(i));
    }
    lc=0;
    localStorage.setItem('lc',lc);

})