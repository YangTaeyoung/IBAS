function getCheckboxValue()  {
  // 선택된 목록 가져오기
  const query = 'input[name="day"]:checked';
  const selectedEls =
      document.querySelectorAll(query);
  // 선택된 목록에서 value 찾기
  let result = '';
  selectedEls.forEach((el) => {
    result += el.value + ' ';
  });
  // 출력
  document.getElementById('result').value = result;
}
