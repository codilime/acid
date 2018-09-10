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
    let all_unfold_ids = sessionStorage.getItem('unfolded_rows')
    let row_id = $(this).attr('id')
    $(this).toggleClass('unfold')
    $(this).parent().toggleClass('active-border')
    row_id = row_id.replace("heading", "collapse")
    if (all_unfold_ids === null) {
      sessionStorage.setItem('unfolded_rows', row_id + ",")
    } else {
      ids = all_unfold_ids.split(',')
      current_id_index = ids.indexOf(row_id)
      if ( current_id_index === - 1) {
        sessionStorage.setItem('unfolded_rows', all_unfold_ids + row_id + ",")
      } else {
        ids.splice(current_id_index,1)
        sessionStorage.setItem('unfolded_rows', ids)
      }
    }
  })

  $(window).ready(function() {
    let all_unfold_ids = sessionStorage.getItem('unfolded_rows')
    ids_to_unfold = all_unfold_ids.split(',')
    for (id of ids_to_unfold){
        $('#'+id).addClass('show')
    }
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
