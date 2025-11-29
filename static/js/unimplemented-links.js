// 未実装リンクの処理
document.addEventListener('DOMContentLoaded', function() {
  // すべての # リンクを取得
  const links = document.querySelectorAll('a[href="#"]');
  
  links.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const title = link.getAttribute('title');
      let message = '未実装です';
      
      if (title === 'スライド') {
        message = '📊 スライドは未実装です\n\nこの章のスライドはまだ準備されていません。';
      } else if (title === '音声解説') {
        message = '🎧 音声解説は未実装です\n\nこの章の音声解説はまだ準備されていません。';
      }
      
      alert(message);
    });
  });
});
