// 打开任意 Wikipedia 页面后在 Console 运行，抓取获奖列表
(async () => {
  // 获取页面 HTML 并解析 wikitables
  const resp = await fetch(
    'https://en.wikipedia.org/w/api.php?origin=*&action=parse&page=Palme_d%27Or&prop=text&format=json'
  );
  const data = await resp.json();
  const doc = new DOMParser().parseFromString(data.parse.text['*'], 'text/html');
  const tables = doc.querySelectorAll('table.wikitable');

  // 找到奖项表格（遍历 wikitables）
  for (const table of tables) {
    const rows = table.querySelectorAll('tr');
    if (rows.length < 5) continue;

    // 读表头
    const headers = [...rows[0].querySelectorAll('th')].map(h => h.textContent.trim());

    // 年份可能在第 0 或第 1 列
    let yearCol = headers.findIndex(h => /year|année|jahr/i.test(h));
    if (yearCol < 0) yearCol = 0;

    // 影片列
    let filmCol = headers.findIndex(h => /film|title|titre/i.test(h));
    if (filmCol < 0) filmCol = 1;

    // 导演列（如果有）
    let dirCol = headers.findIndex(h => /director|réalisateur/i.test(h));
    if (dirCol < 0) dirCol = -1;

    console.log(`Table columns: Year=${yearCol} Film=${filmCol} Director=${dirCol}`);
    console.log(`Headers:`, headers);

    // 逐行解析
    for (let i = 1; i < rows.length; i++) {
      const cells = rows[i].querySelectorAll('td');
      if (cells.length < 2) continue;

      const year = cells[yearCol]?.textContent?.trim();
      const film = cells[filmCol]?.textContent?.trim();
      const director = dirCol >= 0 ? cells[dirCol]?.textContent?.trim() : '';

      // 过滤掉非年份行（如脚注、空行）
      if (!year || isNaN(year) || parseInt(year) < 1990) continue;

      console.log(`${year} — ${film} (${director})`);
    }
  }
})();
