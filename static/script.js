$(function () {
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
    for (let id of idsToUnfold) {
      $('#' + id).addClass('show')
    }
  })

  $(document).ready(function () {
    $('.custom-select').select2({
      placeholder: 'Select branch'
    })
  })
})

function enableAutoRefresh () { // eslint-disable-line no-unused-vars
  let refreshFlag = sessionStorage.getItem('refreshTag')
  $('#auto-refresh-li').removeClass('d-none')
  window.setInterval(refresh, 15000)
  if (refreshFlag == null) {
    sessionStorage.setItem('refreshTag', 'is_off')
  }
  if (refreshFlag === 'is_on' && !$('#auto-refresh').is(':checked')) {
    $('#auto-refresh').click()
  }
  $('#auto-refresh').on('change', function (event) {
    if (sessionStorage.getItem('refreshTag') === 'is_on') {
      sessionStorage.setItem('refreshTag', 'is_off')
    } else {
      sessionStorage.setItem('refreshTag', 'is_on')
    }
  })

  function refresh () {
    if ($('#auto-refresh').is(':checked')) {
      window.location.reload()
    }
  }
}

function unfoldAll () { // eslint-disable-line no-unused-vars
  window.setInterval(unfoldButton, 100)
  $('#unfold-all-li').removeClass('d-none')
  let allUnfoldIds = $('#refs_list').attr("content").replace(/[\[\]'"\ ]/gm, '').split(',').sort().toString()

  function unfoldButton() {
    let currentUnfoldedRows = sessionStorage.getItem('unfoldedRows').split(',').sort()
    let currentUnfoldedRowsString = currentUnfoldedRows.toString()
    if (allUnfoldIds != currentUnfoldedRowsString) {
      if ($('#unfold-all').is(':checked')) {
        sessionStorage.setItem('unfoldedRows', allUnfoldIds)
        window.location.reload()
      }
    }
  }
}
