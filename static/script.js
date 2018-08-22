$(function () {

  $('[data-localtime="true"]').each(function () {
    let $element = $(this)
    let dateTime = moment.utc($element.text().trim())
    dateTime.local()
    $element.text(dateTime.format('YYYY-MM-DD HH:mm:ss'))
  })

  $('.no-collapsable').on('click', function (event) {
    event.stopImmediatePropagation()
  })
})

function RefreshMe () {
  var RefreshF = localStorage.getItem('refresh_f')
  $('#auto-refresh-li').removeClass('d-none')
  window.setInterval(refresh, 30000)
  if (RefreshF == null) {
    localStorage.setItem('refresh_f', 'is_off')
  }
  if (RefreshF === 'is_on' && !$('#auto-refresh').is(':checked')) {
    $('#auto-refresh').click()
  }
  $('#auto-refresh').on('change', function (event) {
    if (RefreshF === 'is_on') {
      localStorage.setItem('refresh_f', 'is_off')
    } else if (RefreshF === 'is_off') {
      localStorage.setItem('refresh_f', 'is_on')
    }
  })

  function refresh () {
    if ($('#auto-refresh').is(':checked')) {
      window.location.reload()
    }
  }
}
