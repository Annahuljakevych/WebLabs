function chord_string(chord_it) {
    let arr = [];
    len = chord_it.length;
    arr.push(chord_it)
    for (let i = 0; i < len; i++)
    {
        chord_it = ' ' + chord_it;
        arr.push(chord_it)
    }
    for (let i = 0; i < len; i++)
    {
        chord_it = chord_it.slice(1);
        arr.push(chord_it)
    }
    return arr
}

var X = chord_string('$$$$$');
for (var i of X) {
    console.log(i)
}