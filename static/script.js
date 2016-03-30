STATUS = ['OK', 'Compiling', 'Running', 'Compilation error']

$("#refresh-table").click(refresh_table = function() {
  $.ajax({
    url: "get-solutions",
    success: function(solutions) {
      for (i = 0; i < solutions.length; ++i)
        solutions[i].status = STATUS[solutions[i].status]
      $("#solutions-table").html($("#solutions-template").tmpl({ solutions }))
    }
  })
})

$("#send-code").click(function() {
  source_code = $("#source-code").val()
  test = $("#test").val()
  lang = $("#langs-list").val()
  time_limit = $("#time-limit").val()
  memory_limit = $("#memory-limit").val()
  $.post({
    url: "send-code",
    data: { source_code, test, lang, time_limit, memory_limit },
    success: function(data) {
      alert("OK")
      refresh_table()
    }
  })
})

function make_langs_list() {
  $.ajax({
    url: "get-langs",
    success: function(langs) {
      $("#langs-list").html($("#langs-list-template").tmpl({ langs }))
    }
  })
}

make_langs_list()
refresh_table()
