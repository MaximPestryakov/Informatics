STATUS = ['OK', 'Compiling', 'Running', 'Compilation error', 'Time limit', 'Runtime error', 'Memory limit', 'Queue', 'Check Failed']

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
  cpu_time_limit = $("#cpu-time-limit").val()
  real_time_limit = $("#real-time-limit").val()
  memory_limit = $("#memory-limit").val()
  $.post({
    url: "send-code",
    data: { source_code, test, lang, cpu_time_limit, real_time_limit, memory_limit },
    success: function(data) {
      if (data.code == 0)
        alert("OK")
      else if (data.code == 1)
        alert("Type error")
      else if (data.code == 2)
        alert("Value error")
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
