$(function () {
  if (sessionStorage.getItem('unfoldedRows') === null) {
    sessionStorage.setItem('unfoldedRows', '')
  }
  $('[data-localtime="true"]').each(function () {
    let $element = $(this)
    let dateTime = moment.utc($element.text().trim())
    dateTime.local()
    $element.text(dateTime.format('YYYY-MM-DD HH:mm:ss'))
  })

  $('.no-collapsible').on('click', function (event) {
    event.stopImmediatePropagation()
  })

  $('.clickable').click(function () {
    let $item = $(this)

    let allUnfoldIds = sessionStorage.getItem('unfoldedRows')
    let rowId = $item.attr('id')
    let newSessionStorageValue = []

    $item.toggleClass('unfold')
    $item.parent().toggleClass('active-border')

    rowId = rowId.replace('heading', 'collapse')

    if (allUnfoldIds === null) {
      newSessionStorageValue.push(rowId)
    } else {
      let ids = allUnfoldIds.split(',')
      newSessionStorageValue = ids
      if (ids.indexOf(rowId) === -1) {
        newSessionStorageValue.push(rowId)
      } else {
        newSessionStorageValue = ids.filter(item => item !== rowId)
      }
    }
    newSessionStorageValue = newSessionStorageValue.filter(item => item !== '')
    sessionStorage.setItem('unfoldedRows', newSessionStorageValue)
  })
  $(window).ready(function () {
    let allUnfoldIds = sessionStorage.getItem('unfoldedRows')
    let idsToUnfold = allUnfoldIds.split(',')
    idsToUnfold.forEach(expand)
  })

  $(document).ready(function () {
    $('.custom-select').select2({
      placeholder: 'Select branch'
    })
  })
})

function enableAutoRefresh() { // eslint-disable-line no-unused-vars
  window.setInterval(refresh, 15000)
  function refresh() {
    if (sessionStorage.getItem('refreshTag') === 'is_on') {
      window.location.reload()
    }
  }
}

function turnOnAutoRefresh() { // eslint-disable-line no-unused-vars
  sessionStorage.setItem('refreshTag', 'is_on')
}

function turnOffAutoRefresh() { // eslint-disable-line no-unused-vars
  sessionStorage.setItem('refreshTag', 'is_off')
}

function unfoldAll() { // eslint-disable-line no-unused-vars
  $('#unfold-all-li').removeClass('d-none')
  let allIds = $('#refs_list').attr('content')
    .replace(/[\[\]'"\ ]/gm, '')
    .split(',')
    .sort()
    .toString()
  let idsToUnfold = allIds.split(',')
  let newSessionStorageValue = ''

  $('#unfold-all').on('click', function (event) {
    let currentUnfoldedRowsArray = sessionStorage.getItem('unfoldedRows').split(',')
    if ($(this)[0].checked) {
      newSessionStorageValue = allIds
    } else {
      newSessionStorageValue = ''
    }
    let diffArray = idsToUnfold.filter(x => !currentUnfoldedRowsArray.includes(x))
    if (diffArray.length === 0) {
      diffArray = idsToUnfold
    }
    diffArray.forEach(expand)
    sessionStorage.setItem('unfoldedRows', newSessionStorageValue)
  })

  $('.clickable').click(function () {
    $('#unfold-all').prop('checked', false)
  })
}

function expand(id) {
  $('#' + id).toggleClass('show').parent().toggleClass('active-border')
  id = id.replace('collapse', 'heading')
  $('#' + id).toggleClass('unfold').toggleClass('collapsed')
}

function displayFlash() { // eslint-disable-line no-unused-vars
  setTimeout(() => {
    $('.flashes').addClass('flashes-active')
  }, 100)
  setTimeout(() => {
    $('.flashes').removeClass('flashes-active')
  }, 5000)
}