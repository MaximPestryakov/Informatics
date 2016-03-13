STATUS = ['OK', 'Compiling', 'Running', 'Compilation error']

$("#refresh_table").click(refresh_table = function() {
  $.ajax({
    url: "get-solutions",
    success: function(solutions) {
      for (i = 0; i < solutions.length; ++i)
        solutions[i].status = STATUS[solutions[i].status]
      $("#solutions-table").html($("#solutions-template").tmpl({ solutions }))
    }
  })
})

$("#send_code").click(function() {
  source_code = $("#source-code").val()
  test = $("#test").val()
  lang = $("#langs-list").val()
  $.post({
    url: "send-code",
    data: { source_code, test, lang },
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
