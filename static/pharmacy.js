function amount(){
    var a=document.getElementById('amount').value;
    var b=document.getElementById('quantity').value;
    console.log(a);
    console.log(b);
    var c=250*b;
    document.getElementById('bill-amt').innerHTML=c;
    
}