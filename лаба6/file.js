class PhotoGallery extends HTMLElement {
	constructor() {
		super()
		const shadow = this.attachShadow({ mode: "open" });
		const div = document.createElement("div");
		div.setAttribute("id", "photo-gallery");
		shadow.appendChild(div);
		const style = document.createElement("style");
		style.innerHTML = `
		#photo-gallery
		{
			display: flex;
			flex-wrap: wrap;
			justify-content: center;
		}
		#photo-gallery div
		{
			width: 200px;
			height: 200px;
			margin: 1px;
			display: flex;
			overflow: hidden;
			align-items: center;
			justify-content: center;
		}
		#photo-gallery div#fullscreen
		{
			position: fixed;
			height: 100vh;
			width: 100vw;
			transition: all 2s ease-in-out;
			z-index: 1;
		}`;
		shadow.appendChild(style);
		if (this.hasAttribute("pic-list")) {
			let piclist = this.getAttribute("pic-list").split(';');
			for (let i of piclist) {
				const element = document.createElement("div");
				element.setAttribute("onclick", "fullscreen(this)")
				const pic = document.createElement("img");
				pic.setAttribute("onerror", "this.src = 'https://www.hoaxuantravel.com/images/icon/error.png'")
				pic.setAttribute("onload", "calc_size(this)")
				pic.setAttribute("src", i);
				element.appendChild(pic);
				div.appendChild(element);
			}
		}
	}
}

function calc_size(img) {
	let img_pos = img.getBoundingClientRect();
	if (img_pos.height <= img_pos.width) {
		img.style.height = '100%';
		img.style.width = 'auto';
	}
	if (img_pos.height > img_pos.width) {
		img.style.height = 'auto';
		img.style.width = '100%';
	}
}

customElements.define("photo-gallery", PhotoGallery);

let full = false;
let gallerystyle = '';
function fullscreen(pic) {
	if (!full) {
		full = true;
		pic.setAttribute("id", "fullscreen");
		gallerystyle = pic.firstChild.getAttribute("style");
		pic.firstChild.setAttribute("style", "height:95vh;");
	}
	else {
		pic.setAttribute("id", "");
		pic.firstChild.setAttribute("style", gallerystyle);
		full = false;
	}
}

document.body.onload = function () {
	setTimeout(function () {
		let preloader = document.getElementById("preloader");
		preloader.style.visibility = "hidden";
	}, 1500)
}