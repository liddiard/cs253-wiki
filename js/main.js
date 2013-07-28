function invalidField(args) {
    for (var i = 0; i < arguments.length; i++) {
        $(arguments[i]+'-msg').show();
    }
    
    if (arguments.length === 0) {
        $('#username').focus()
    } else {
        $(arguments[0]).focus(); //set focus on the first invalid field
    }

    var count = 0;
    function toggleBorder(args) {
        count++;
        for (var j = 0; j < args.length; j++) {
                $(args[j]).toggleClass("invalid-input");
            }
        if (count < 5) {
            setTimeout(toggleBorder(args), 500);
        }
    }

    setTimeout(toggleBorder(arguments), 500);
}