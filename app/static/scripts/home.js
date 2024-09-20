const groupsIcon = document.querySelector('#groups-icon')
const chatsIcon = document.querySelector('#chats-icon')
const groupsList = document.querySelector('#groups-list')
const chatsList = document.querySelector('#chats-list')
const calendarIcon = document.querySelector('#calendar-icon')
const calendarSchedules = document.querySelector('#calendar-schedules')
const mobileNotifications = document.querySelector('#mobile-notifications')

groupsIcon.addEventListener('click', () => {
	if (window.location.pathname !== '/home') {
		window.location.href = 'http://' + window.location.host + '/home'
	} 
	groupsIcon.classList.add('border-b-2')
	chatsIcon.classList.remove('border-b-2')
	calendarIcon.classList.remove('border-b-2')
	chatsList.classList.add('hidden')
	calendarSchedules.classList.add('hidden')
	groupsList.classList.remove('hidden')
	mobileNotifications.classList.add('hidden')
})

chatsIcon.addEventListener('click', () => {
	if (window.location.pathname !== '/home') async () => {
		window.location.href = 'http://' + window.location.host + '/home'
	}
	window.location.hash = 'chats'
	chatsIcon.classList.add('border-b-2')
	groupsIcon.classList.remove('border-b-2')
	calendarIcon.classList.remove('border-b-2')
	groupsList.classList.add('hidden')
	chatsList.classList.remove('hidden')
	calendarSchedules.classList.add('hidden')
	mobileNotifications.classList.add('hidden')
})

calendarIcon.addEventListener('click', () => {
	if (window.location.pathname !== '/home') {
		window.location.href = 'http://' + window.location.host + '/home'
	}
	window.location.hash = 'calendar'
	chatsIcon.classList.remove('border-b-2')
	groupsIcon.classList.remove('border-b-2')
	calendarIcon.classList.add('border-b-2')
	groupsList.classList.add('hidden')
	chatsList.classList.add('hidden')
	calendarSchedules.classList.remove('hidden')
	mobileNotifications.classList.add('hidden')
})

window.onload = () => {
	if (window.location.hash) {
		document.querySelector(window.location.hash).click()
	}
}