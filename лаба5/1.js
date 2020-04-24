console.log("  Italian fiscal code  ");
class Person {
    constructor(name, surname, gender, date)
    {
        this.name = name;
        this.surname = surname;
        this.gender = gender;
        this.date = date;
    }
}

//Повертає слово без голосних букв
function removeVowels(word) {
    return word.replace(/[aeiouy]/g, "");
}

//Повертає слово без приголосних букв
function removeConsonant(word) {
    return word.replace(/[bcdfghjklmnpqrstvwxz]/g, "");
}

function personSurname(input) {
   var ThreeSymbols = "";
    if (input.length < 3) {//Якщо менше трьох літер тоді "X" займе третю позицію після приголосного та голосного
        ThreeSymbols += removeVowels(input) + removeConsonant(input) + "X";
        return ThreeSymbols;
    }
    if (removeVowels(input).length >= 3) { //Якщо більше 3 приголосних виводимо перші 3
        for (var i = 0; i < 3; i++) {
            ThreeSymbols += removeVowels(input)[i];
        }
        return ThreeSymbols;
    }
    if (removeVowels(input).length < 3) {//Якщо менше 3 приголосних, в кінець додаємо голосні
        ThreeSymbols += removeVowels(input);
        for (var i = 0; i < 3; i++) {
            if (ThreeSymbols.length != 3) {
                ThreeSymbols += removeConsonant(input)[i];
            } else {
                ThreeSymbols += "X";
            }
        }
        return ThreeSymbols;
    }
}
function personName(input) {
    var ThreeSymbols = "";
    if (input.length < 3) {//Менше трьох літер тоді "X" займе третю позицію після приголосного та голосного
        ThreeSymbols += removeVowels(input) + removeConsonant(input) + "X";
        return ThreeSymbols;
    }
    if (removeVowels(input).length < 3) {//Менше трьох приголосних, тоді голосні замінять відсутні літери в тому ж порядку, в якому вони відображаються 
        ThreeSymbols += removeVowels(input);
        for (var i = 0; i < 3; i++) {
            if (ThreeSymbols.length != 3) {
                ThreeSymbols += removeConsonant(input)[i];
            } else {
                break;
            }
        }
        return ThreeSymbols;
    }
    if (removeVowels(input).length == 3) { //Рівно 3 приголосних тоді приголосні вживаються в тому порядку, в якому вони з’являються 
        for (i = 0; i < 3; i++) {
            ThreeSymbols += removeVowels(input)[i];
        }
        return ThreeSymbols;
    }
    if (removeVowels(input).length > 3) { //Вживається більше 3 приголосних, тоді перший, третій та четвертий приголосні
        ThreeSymbols += removeVowels(input)[0] + removeVowels(input)[2] + removeVowels(input)[3];
        return ThreeSymbols;
    }
}

const months = { 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "H", 7: "L", 8: "M", 9: "P", 10: "R", 11: "S", 12: "T" }
var a = new Person('Ann', 'Mo', 'T', '12/11/1999');
console.log(a);

function gender_date(gen, dat) {
    var data = "";
    var rec = "";
    for (i = 0; i < 2; i++) {
        data = dat.split('/');
    }
    day = data[0];
    month = data[1];
    year = data[2];
    rec = year.substr(-2);
    rec += months[month];
    if (gen == "M") {
        if (day < 10) {
            rec += "0" + day;
        } else {
            rec += day;
        }
    } else {
        var newday = +day;
        newday += 40;
        rec += newday;
    }
    return (rec);
}
console.log("Task 1");
console.log("Person:");
console.log(personSurname(a.surname) + personName(a.name) + gender_date(a.gender, a.date));
