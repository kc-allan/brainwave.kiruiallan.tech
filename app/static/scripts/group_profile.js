const filesNav = document.querySelector('#members-nav')
const membersNav = document.querySelector('#files-nav')
const filesList = document.querySelector('#members-list')
const membersList = document.querySelector('#files-list')
filesNav.addEventListener('click', () => {
	membersNav.classList.remove('border-b-black')
	filesNav.classList.add('border-b-black')
	filesList.classList.remove('hidden')
	membersList.classList.add('hidden')
})

membersNav.addEventListener('click', () => {
	membersNav.classList.add('border-b-black')
	filesNav.classList.remove('border-b-black')
	membersList.classList.remove('hidden')
	filesList.classList.add('hidden')
})

const onSearchUsers = () => {
	const input = document.querySelector('#search-members')
	const filter = input.value.toUpperCase()

	const list = document.querySelectorAll('#members li')

	list.forEach((elem) => {
		const text = elem.textContent.toUpperCase().trim().trimEnd();
		elem.style.display = text.includes(filter) ? 'grid' : "none";
	})
}

document.querySelector('#search-members').addEventListener('input', () => {
	onSearchUsers()
})