var pace=111;
var k=0;
var text="weeknd";
var count=0;
function effect()
{
    if(k<text.length){
        document.getElementById("typ").innerHTML+=text.charAt(k);
        setTimeout(effect,pace);
        k++;
    }
    else
    {
        count++;
        effect2();
    }

    // while(k>=0){
    //     document.getElementById("typ").innerHTML=text.slice(0,k);
    //     setTimeout(effect,pace);
    //     k--;
    // }
    // if(k>3){
    //     document.getElementById("typ").innerHTML=
    // }
//    if(k<)
}
function effect2()
{
    if(k>=0){
        document.getElementById("typ").innerHTML=text.slice(0,k);
        setTimeout(effect2,pace);
        k--;
    }
    else
    {
        if(count==1)
        text="knowing";
        else if(count==2)
        text="zone";
        else
        {
            count=0;
            text="weeknd";
        }
        effect();
    }
}