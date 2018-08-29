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

$('.clickable').click(function () {
  $(this).toggleClass('unfold')
  $(this).parent().toggleClass('active-border')
})
