function Ceasar(string, num) {
	if (num < 0) {
		return Ceasar(string, num + 26)
	}
	cipher = ''
	for (i = 0; i < string.length; i++) {
		cip = string[i]
		code = string.charCodeAt(i)
		if (cip.match(/[a-z]/i)) {
			if ((code >= 65) && (code <= 90)) {
				cip = String.fromCharCode(((code - 65 + num) % 26) + 65)
			}
			else if ((code >= 97) && (code <= 122)) {
				cip = String.fromCharCode(((code - 97 + num) % 26) + 97)
			}
		}
		cipher += cip
	}
	return cipher
}

console.log(Ceasar("Always-Look-on-the-Bright-Side-of-Life", 5))