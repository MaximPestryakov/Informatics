STATUS = ["OK"]
LANG = ["GNU C++ 4.9", "Java JDK 1.7", "Python 3.3"]
solutions_table = $("#solutions-table").html()

$("#send_code").click(function() {
  source_code = $("#source-code").val()
  test = $("#test").val()
  lang = $("#langs-list").val()
  $.post({
    url: "send-code",
    data: { source_code, test, lang },
    success: function(data) {
      alert("OK")
    }
  });
})

$("#refresh_table").click(function() {
  jQuery.ajax({
    url: "get-solutions",
    success: function(solutions) {
      solutions.forEach(function(object) {
        object.status = STATUS[object.status - 1]
        object.lang = LANG[object.lang - 1]
      })
      $("#solutions-template").tmpl({ solutions }).appendTo("#solutions-table")
    }
  })
})
