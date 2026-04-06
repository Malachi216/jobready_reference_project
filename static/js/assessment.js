
let currentQuestionIndex = 0;
let totalQuestions = 0;
let answers = {};

function escapeHtml(text) {
  const map = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'};
  return String(text).replace(/[&<>"']/g, m => map[m]);
}

document.addEventListener('DOMContentLoaded', function() {
  const savedProfile = sessionStorage.getItem('userProfile');
  if (!savedProfile) {
    window.location.href = '/profile';
    return;
  }

  const urlParams = new URLSearchParams(window.location.search);
  const explorationCareers = urlParams.get('careers');
  if (explorationCareers) {
    startExplorationAssessment(explorationCareers.split(','));
  } else {
    startRegularAssessment();
  }

  document.getElementById('next-btn').addEventListener('click', goToNextQuestion);
  document.getElementById('back-btn').addEventListener('click', goToPreviousQuestion);
});

function startRegularAssessment() {
  fetch('/api/clear-cache', {method: 'POST'})
    .then(r => r.json())
    .then(() => fetch('/api/generate-assessment', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({assessment_type:'initial'})
    }))
    .then(r => r.json())
    .then(data => {
      if (data.success) loadCurrentQuestion();
      else alert('Could not generate assessment.');
    })
    .catch(err => {
      console.error(err);
      alert('Error generating assessment.');
    });
}

function startExplorationAssessment(careers) {
  fetch('/api/start-exploration', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({careers})
  }).then(r => r.json()).then(data => {
    if (data.success) loadCurrentQuestion();
  });
}

function loadCurrentQuestion() {
  fetch('/api/get-current-answers')
    .then(r => r.json())
    .then(answersData => {
      answers = answersData.answers || {};
      return fetch('/api/current-question');
    })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      if (data.finished) {
        window.location.href = '/analyzing';
        return;
      }
      currentQuestionIndex = data.current - 1;
      totalQuestions = data.total;
      document.getElementById('question-category').textContent = data.question.category || 'General';
      document.getElementById('question-text').textContent = data.question.text;
      document.getElementById('progress-text').textContent = `Questions ${data.current} of ${data.total}`;
      document.getElementById('progress-bar-fill').style.width = `${(data.current / data.total) * 100}%`;
      renderOptions(data.question.options, answers[currentQuestionIndex]);
    })
    .catch(err => {
      console.error(err);
      alert('Error loading question.');
    });
}

function renderOptions(options, selectedAnswer) {
  const optionsContainer = document.getElementById('options-container');
  optionsContainer.innerHTML = '';
  options.forEach((option, index) => {
    const optionDiv = document.createElement('div');
    optionDiv.className = 'option';
    const isSelected = selectedAnswer === option;
    optionDiv.innerHTML = `
      <input type="radio" name="option" value="${escapeHtml(option)}" id="option${index}" ${isSelected ? 'checked' : ''}>
      <label for="option${index}">${escapeHtml(option)}</label>
    `;
    optionsContainer.appendChild(optionDiv);
  });
}

function getSelectedAnswer() {
  const options = document.getElementsByName('option');
  for (const option of options) {
    if (option.checked) return option.value;
  }
  return '';
}

function goToNextQuestion() {
  const selectedAnswer = getSelectedAnswer();
  if (!selectedAnswer) {
    alert('Please select an answer before proceeding.');
    return;
  }
  answers[currentQuestionIndex] = selectedAnswer;
  const nextBtn = document.getElementById('next-btn');
  nextBtn.disabled = true;
  nextBtn.textContent = 'Loading...';
  fetch('/api/next-question', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({answer: selectedAnswer})
  })
    .then(r => r.json())
    .then(data => {
      if (data.finished) window.location.href = '/analyzing';
      else loadCurrentQuestion();
    })
    .catch(err => {
      console.error(err);
      alert('Error submitting answer.');
    })
    .finally(() => {
      nextBtn.disabled = false;
      nextBtn.textContent = 'Next';
    });
}

function goToPreviousQuestion() {
  fetch('/api/go-to-previous', {method:'POST'})
    .then(r => r.json())
    .then(() => loadCurrentQuestion())
    .catch(err => console.error(err));
}
