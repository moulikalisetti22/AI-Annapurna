document.addEventListener('DOMContentLoaded', () => {
  const voiceButtons = document.querySelectorAll('[data-voice]');
  const welcomeMessage = "FoodBridge is ready. You can donate food, find food, and support your community.";

  const speak = (text) => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-IN';
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    }

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-IN';
      recognition.start();
    }
  };

  voiceButtons.forEach((button) => {
    button.addEventListener('click', () => speak(button.dataset.voice || welcomeMessage));
  });

  const flash = document.querySelector('.flash');
  if (flash) {
    setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-6px)';
      setTimeout(() => flash.remove(), 260);
    }, 3500);
  }
});
