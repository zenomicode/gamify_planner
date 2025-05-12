// Получаем элементы DOM
const findTeamBtn = document.getElementById('findTeamBtn');
const createTeamBtn = document.getElementById('createTeamBtn');
const findTeamModal = document.getElementById('findTeamModal');
const createTeamModal = document.getElementById('createTeamModal');
const joinTeamBtn = document.getElementById('joinTeamBtn');
const confirmCreateBtn = document.getElementById('confirmCreateBtn');

// Открытие модальных окон
findTeamBtn.addEventListener('click', () => {
  findTeamModal.style.display = 'block';
});

createTeamBtn.addEventListener('click', () => {
  createTeamModal.style.display = 'block';
});

// Закрытие модальных окон при клике вне их области
window.addEventListener('click', (event) => {
  if (event.target === findTeamModal) {
    findTeamModal.style.display = 'none';
  }
  if (event.target === createTeamModal) {
    createTeamModal.style.display = 'none';
  }
});

// Обработчики для кнопок в модальных окнах
joinTeamBtn.addEventListener('click', () => {
  findTeamModal.style.display = 'none';
});

confirmCreateBtn.addEventListener('click', () => {
  createTeamModal.style.display = 'none';
});