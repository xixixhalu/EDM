//copy code to clipboard
function CopyToClipboard(containerid) {
    // Create a new textarea element and give it id='t'
    var textarea = document.createElement('textarea');
    textarea.id = 't';
    // Optional step to make less noise on the page, if any!
    textarea.style.height = 0;
    // Now append it to your page somewhere, I chose <body>
    document.body.appendChild(textarea);
    // Give our textarea a value of whatever inside the div of id=containerid
    textarea.value = document.getElementById(containerid).innerText;
    // Now copy whatever inside the textarea to clipboard
    var selector = document.querySelector('#t');
    selector.select();
    document.execCommand('copy');
    // Remove the textarea
    document.body.removeChild(textarea);
    alert("Your code has been copied to clipboard");
}

//display line numbers:
// (function() {
//     var pre = document.getElementsByTagName('pre'),
//         pl = pre.length;
//     for (var i = 0; i < pl; i++) {
//         pre[i].innerHTML = '<span class="line-number"></span>' + pre[i].innerHTML
//             + '<span class="cl"></span>';
//         var num = pre[i].innerHTML.split(/\r\n/).length;
//         for (var j = 0; j < num; j++) {
//             var line_num = pre[i].getElementsByTagName('span')[0];
//             line_num.innerHTML += '<span>' + (j + 1) + '</span>';
//         }
//     }
// })();