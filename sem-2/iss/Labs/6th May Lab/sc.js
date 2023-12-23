var pace=111;
var ks=0;
var textstart="the ";
function effectstart()
{
    if(ks<textstart.length){
        document.getElementById("start").innerHTML+=textstart.charAt(ks);
        setTimeout(effectstart,pace);
        ks++;
    }
    else {
    effect();
    }
}