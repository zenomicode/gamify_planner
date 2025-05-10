    // Хранилище задач
    let tasks = [];
    let currentEditingTaskId = null;
    
    // Отображение текущей даты
    function updateCurrentDate() {
      const now = new Date();
      const options = { day: 'numeric', month: 'long' };
      const dateString = now.toLocaleDateString('ru-RU', options);
      document.getElementById('current-date').textContent = `(${dateString})`;
    }
    
    // Генерация ID для задачи
    function generateId() {
      return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    // Отображение задач в каталоге
    function renderTasks() {
      const tasksList = document.getElementById('tasks-list');
      tasksList.innerHTML = '';
      
      tasks.forEach(task => {
        const taskItem = document.createElement('li');
        taskItem.className = 'task-item';
        taskItem.dataset.taskId = task.id;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        checkbox.checked = task.completed;
        
        const taskText = document.createElement('span');
        taskText.className = 'task-text' + (task.completed ? ' completed' : '');
        taskText.textContent = task.text;
        
        checkbox.addEventListener('change', function() {
          task.completed = this.checked;
          taskText.classList.toggle('completed', this.checked);
          saveTasksToLocalStorage();
        });
        
        taskItem.appendChild(checkbox);
        taskItem.appendChild(taskText);
        tasksList.appendChild(taskItem);
        
        // Обработчик для редактирования задачи
        taskItem.addEventListener('click', (e) => {
          if (e.target !== checkbox) {
            editTask(task.id);
          }
        });
      });
      
      renderCalendar();
    }
    
    // Отображение календаря
    function renderCalendar() {
      const calendarContent = document.getElementById('calendar-content');
      calendarContent.innerHTML = '';
      
      // Группировка задач по датам
      const tasksByDate = {};
      
      tasks.forEach(task => {
        // Задачи с дедлайном
        if (task.deadline) {
          const dateStr = new Date(task.deadline).toLocaleDateString('ru-RU');
          if (!tasksByDate[dateStr]) {
            tasksByDate[dateStr] = [];
          }
          tasksByDate[dateStr].push(task);
        }
        
        // Задачи с повторениями
        if (task.repeatDays && task.repeatDays.length > 0) {
          const daysMap = { mon: 'Понедельник', tue: 'Вторник', wed: 'Среда', 
                          thu: 'Четверг', fri: 'Пятница', sat: 'Суббота', sun: 'Воскресенье' };
          
          task.repeatDays.forEach(day => {
            const dayName = daysMap[day];
            if (!tasksByDate[dayName]) {
              tasksByDate[dayName] = [];
            }
            tasksByDate[dayName].push(task);
          });
        }
      });
      
      // Сортировка дат
      const sortedDates = Object.keys(tasksByDate).sort((a, b) => {
        // Если это дни недели, сортируем по порядку
        const daysOrder = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];
        if (daysOrder.includes(a) && daysOrder.includes(b)) {
          return daysOrder.indexOf(a) - daysOrder.indexOf(b);
        }
        // Если это даты, сортируем по дате
        return new Date(a) - new Date(b);
      });
      
      // Отображение задач в календаре
      sortedDates.forEach(date => {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        const dateElement = document.createElement('div');
        dateElement.className = 'calendar-date';
        dateElement.textContent = date;
        dayElement.appendChild(dateElement);
        
        tasksByDate[date].forEach(task => {
          const taskElement = document.createElement('div');
          taskElement.className = 'task-item';
          taskElement.style.margin = '5px 0';
          taskElement.textContent = task.text;
          dayElement.appendChild(taskElement);
        });
        
        calendarContent.appendChild(dayElement);
      });
    }
    
    // Открытие модального окна для новой задачи
    function openNewTaskModal() {
      currentEditingTaskId = null;
      document.getElementById('task-modal-title').textContent = 'Новая задача';
      document.getElementById('task-input').value = '';
      document.getElementById('deadline-input').value = '';
      document.querySelectorAll('input[name="repeat-days"]').forEach(cb => cb.checked = false);
      document.getElementById('delete-task-btn').style.display = 'none';
      document.getElementById('task-modal').style.display = 'flex';
      document.getElementById('task-input').focus();
    }
    
    // Открытие модального окна для редактирования задачи
    function editTask(taskId) {
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      
      currentEditingTaskId = taskId;
      document.getElementById('task-modal-title').textContent = 'Редактировать задачу';
      document.getElementById('task-input').value = task.text;
      document.getElementById('deadline-input').value = task.deadline ? new Date(task.deadline).toISOString().substr(0, 10) : '';
      
      document.querySelectorAll('input[name="repeat-days"]').forEach(cb => {
        cb.checked = task.repeatDays ? task.repeatDays.includes(cb.value) : false;
      });
      
      document.getElementById('delete-task-btn').style.display = 'block';
      document.getElementById('task-modal').style.display = 'flex';
      document.getElementById('task-input').focus();
    }
    
    // Сохранение задачи
    function saveTask() {
      const text = document.getElementById('task-input').value.trim();
      if (!text) return;
      
      const deadline = document.getElementById('deadline-input').value || null;
      const repeatDays = Array.from(document.querySelectorAll('input[name="repeat-days"]:checked'))
                           .map(cb => cb.value);
      
      // Проверка, что не выбраны одновременно дедлайн и повторения
      if (deadline && repeatDays.length > 0) {
        alert('Нельзя одновременно выбрать дедлайн и повторения!');
        return;
      }
      
      const taskData = {
        text,
        deadline: deadline ? new Date(deadline).toISOString() : null,
        repeatDays: repeatDays.length > 0 ? repeatDays : null,
        completed: false
      };
      
      if (currentEditingTaskId) {
        // Редактирование существующей задачи
        const taskIndex = tasks.findIndex(t => t.id === currentEditingTaskId);
        if (taskIndex !== -1) {
          tasks[taskIndex] = { ...tasks[taskIndex], ...taskData };
        }
      } else {
        // Добавление новой задачи
        taskData.id = generateId();
        tasks.push(taskData);
      }
      
      saveTasksToLocalStorage();
      renderTasks();
      document.getElementById('task-modal').style.display = 'none';
    }
    
    // Удаление задачи
    function deleteTask() {
      if (!currentEditingTaskId) return;
      
      tasks = tasks.filter(t => t.id !== currentEditingTaskId);
      saveTasksToLocalStorage();
      renderTasks();
      document.getElementById('task-modal').style.display = 'none';
    }
    
    // Сохранение задач в localStorage
    function saveTasksToLocalStorage() {
      localStorage.setItem('tasks', JSON.stringify(tasks));
    }
    
    // Загрузка задач из localStorage
    function loadTasksFromLocalStorage() {
      const savedTasks = localStorage.getItem('tasks');
      if (savedTasks) {
        tasks = JSON.parse(savedTasks);
      }
      renderTasks();
    }
    
    // Обработчики событий
    document.getElementById('add-task-btn').addEventListener('click', openNewTaskModal);
    
    document.getElementById('cancel-task-btn').addEventListener('click', function() {
      document.getElementById('task-modal').style.display = 'none';
    });
    
    document.getElementById('save-task-btn').addEventListener('click', saveTask);
    
    document.getElementById('delete-task-btn').addEventListener('click', deleteTask);
    
    // Обработчики модального окна каталогов
    document.getElementById('create-catalog-btn').addEventListener('click', function() {
      document.getElementById('catalog-modal').style.display = 'flex';
      document.getElementById('catalog-input').focus();
    });
    
    document.getElementById('cancel-catalog-btn').addEventListener('click', function() {
      document.getElementById('catalog-modal').style.display = 'none';
      document.getElementById('catalog-input').value = '';
    });
    
    document.getElementById('save-catalog-btn').addEventListener('click', function() {
      const catalogName = document.getElementById('catalog-input').value.trim();
      if (catalogName) {
        alert(`Создан новый каталог: ${catalogName}`);
        document.getElementById('catalog-modal').style.display = 'none';
        document.getElementById('catalog-input').value = '';
      }
    });
    
    window.addEventListener('click', function(event) {
      if (event.target.className === 'modal') {
        event.target.style.display = 'none';
      }
    });
    
    // Инициализация
    document.addEventListener('DOMContentLoaded', function() {
      updateCurrentDate();
      loadTasksFromLocalStorage();
      
      // Примеры задач для демонстрации
      if (tasks.length === 0) {
        tasks = [
          {
            id: generateId(),
            text: 'Сделать диплом',
            deadline: new Date(Date.now() + 86400000 * 7).toISOString(), // +7 дней
            repeatDays: null,
            completed: false
          },
          {
            id: generateId(),
            text: 'Полить цветы',
            deadline: null,
            repeatDays: ['mon', 'wed', 'fri'],
            completed: false
          },
          {
            id: generateId(),
            text: 'Дойти на почту на улице Седова и отправить посылку',
            deadline: null,
            repeatDays: null,
            completed: false
          }
        ];
        saveTasksToLocalStorage();
        renderTasks();
      }
    });