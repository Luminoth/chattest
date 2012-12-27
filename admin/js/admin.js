function rollover(object)
{
    if(object.disabled == true || object.src == "" || object.src.indexOf("-over.gif") != -1)
        return;

    object.src = object.src.substring(0, object.src.length - 4) + '-over.gif';
}

function rollout(object)
{
    if(object.disabled == true || object.src == "" || object.src.indexOf("-over.gif") == -1)
        return;

    object.src = object.src.substr(0, object.src.length - 9) + '.gif';
}

function selectAll(boxes, checked, id)
{
    if(boxes == null)
        return;

    var length = boxes.length;
    if(length == 0) {
        if(id == null || boxes.id.indexOf(id) != -1)
            boxes.checked = checked;
    } else {
        for(var i=0; i<length; ++i) {
            if(id == null || boxes[i].id.indexOf(id) != -1)
                boxes[i].checked = checked;
        }
    }
}

function shouldSelectAll(boxes)
{
    var length = boxes.length;
    if(length == 0) return boxes.checked;

    for(var i=0; i<length; ++i) {
        if(boxes[i].checked)
            return false;
    }
    return true;
}

function countSelected(select, maxNumber, selectedOptions)
{
    for(var i=0; i<select.options.length; i++) {
        if(select.options[i].selected && !new RegExp(i,'g').test(selectedOptions.toString())) {
            selectedOptions.push(i);
        }

        if(!select.options[i].selected && new RegExp(i,'g').test(selectedOptions.toString())) {
            selectedOptions = selectedOptions.sort(function(a,b) {return a-b;});
            for(var j=0; j<selectedOptions.length; j++) {
                if(selectedOptions[j] == i) {
                    selectedOptions.splice(j,1);
                }
            }
        }

        if(selectedOptions.length > maxNumber) {
            /*alert('You may only choose ' + maxNumber + ' options!!');*/
            select.options[i].selected = false;
            selectedOptions.pop();
            if(document.all) document.body.focus();
        }
    }
}

/* validation methods */

function dateOnly(e)
{
    // get the key pressed
    var key;
    if(window.event) key = window.event.keyCode;
    else if(e) key = e.which;
    else return true;

    // get the character as a string
    var keychar = String.fromCharCode(key);

    // make sure it's a valid character
    if((key==null) || (key==0) || (key==8) || (key==9) || (key==13) || (key==27))
        return true;
    else if((("0123456789/").indexOf(keychar) > -1))
        return true;

    return false;
}

function timeOnly(e)
{
    // get the key pressed
    var key;
    if(window.event) key = window.event.keyCode;
    else if(e) key = e.which;
    else return true;

    // get the character as a string
    var keychar = String.fromCharCode(key);

    // make sure it's a valid character
    if((key==null) || (key==0) || (key==8) || (key==9) || (key==13) || (key==27))
        return true;
    else if((("0123456789:").indexOf(keychar) > -1))
        return true;

    return false;
}
