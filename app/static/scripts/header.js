const dropdwn = document.querySelectorAll('#dropdown')

dropdwn.forEach((elem) => {
	elem.addEventListener('click', (event) => {
		if (elem.querySelector('#toggle')) {
			elem.querySelector('#toggle').classList.toggle('rotate')	
		}
		elem.querySelector('ul').classList.toggle('active')
		// elem.querySelector('ul').classList.toggle('z-40')
	})
})

const flashed = document.querySelector('#flashed')
if (flashed !== null) {
	setTimeout(() => {
		flashed.classList.add('hidden')
	}, 5000)
}

const hamMenu = document.querySelector('#ham-menu')
const navMenu = document.querySelector('#nav-menu')
hamMenu.addEventListener('click', () => {
	hamMenu.classList.toggle('active')
	navMenu.classList.toggle('hidden')
})

const groupIcon = document.querySelector('#groups-icon')
const chatIcon = document.querySelector('#chats-icon')
const scheduleIcon = document.querySelector('#calendar-icon')

const icons = [groupIcon, chatIcon, scheduleIcon]

icons.forEach((icon) => {
	icon.addEventListener('click', () => {
		if (window.location.pathname !== '/home') {
			window.location.href = 'http://' + window.location.host + '/home#' + icon.id
		}
	})
})