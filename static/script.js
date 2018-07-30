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
