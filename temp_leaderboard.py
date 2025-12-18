from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
start = text.index('function loadLeaderboard')
end = text.index('\n  // Quiz', start)
old = text[start:end]
new = """function loadLeaderboard() {
    const leaderboardContainer = document.getElementById('leaderboardContainer');
    leaderboardContainer.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-light);">Loading leaderboard...</div>';
    const usersRef = ref(db, 'users');

    onValue(usersRef, (snapshot) => {
      if (!snapshot.exists()) {
        leaderboardContainer.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-light);">No learners yet. Be the first to take a quiz!</div>';
        return;
      }

      const users = [];
      snapshot.forEach((child) => {
        const user = child.val();
        const displayName = user.displayName || (user.email ? user.email.split('@')[0] : 'Learner');
        users.push({
          id: child.key,
          userId: child.key,
          displayName,
          email: user.email || 'unknown',
          highScore: user.highScore || 0,
          totalQuizzes: user.totalQuizzes || 0
        });
      });

      users.sort((a, b) => {
        if (b.highScore !== a.highScore) {
          return b.highScore - a.highScore;
        }
        return (b.totalQuizzes || 0) - (a.totalQuizzes || 0);
      });

      leaderboardContainer.innerHTML = '';
      users.forEach((user, index) => {
        const rank = index + 1;
        const firstLetter = user.displayName.charAt(0).toUpperCase();
        const leaderboardItem = document.createElement('div');
        leaderboardItem.className = 'leaderboard-item';
        leaderboardItem.innerHTML = `
          <div class="rank ${rank <= 3 ? 'rank-' + rank : ''}">${rank}</div>
          <div class="player-info">
            <div class="player-avatar">${firstLetter}</div>
            <div class="player-details">
              <div class="player-name">${user.displayName}</div>
              <div class="player-email">${user.email}</div>
            </div>
          </div>
          <div class="player-score">${user.highScore} pts</div>
        `;

        if (currentUser && user.userId === currentUser.uid) {
          leaderboardItem.style.background = 'rgba(24, 119, 242, 0.1)';
          leaderboardItem.style.borderLeft = '3px solid var(--primary)';
        }

        leaderboardContainer.appendChild(leaderboardItem);
      });
    });
  }

  function loadUserScores() {
    if (!currentUser) return;

    const historyList = document.getElementById('userScoresList');
    if (!historyList) return;

    historyList.innerHTML = '<div class="empty">Loading your scores…</div>';

    const scoresRef = ref(db, 'scores');
    if (userScoresUnsubscribe) {
      userScoresUnsubscribe();
      userScoresUnsubscribe = null;
    }
    userScoresUnsubscribe = onValue(scoresRef, (snapshot) => {
      if (!snapshot.exists()) {
        historyList.innerHTML = '<div class="empty">No quiz history yet. Play a quiz to see it here.</div>';
        return;
      }

      const entries = [];
      snapshot.forEach((child) => entries.push(child.val()));
      const userEntries = entries
        .filter(entry => entry.userId === currentUser.uid)
        .sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));

      if (!userEntries.length) {
        historyList.innerHTML = '<div class="empty">No quiz history yet. Play a quiz to see it here.</div>';
        return;
      }

      historyList.innerHTML = '';
      userEntries.forEach(entry => {
        const entryItem = document.createElement('div');
        entryItem.className = 'score-history-item';
        const playerName = entry.displayName || (entry.email ? entry.email.split('@')[0] : 'Learner');
        const points = entry.points ?? entry.score;
        const date = entry.timestamp ? new Date(entry.timestamp).toLocaleString() : 'Just now';

        entryItem.innerHTML = `
          <div>
            <div class="score-label">${points} pts</div>
            <div class="score-date">${date}</div>
          </div>
          <div class="score-label">${playerName}</div>
        `;

        historyList.appendChild(entryItem);
      });
    });
  }
"""
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('leaderboard block replaced')
