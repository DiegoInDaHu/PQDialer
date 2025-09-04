<?php

$apikey = "VLLkPJVtf3I5UocNmgTTEKSJBGWUjT8T"; //PON AQUI TU API KEY
$origin = "255"; //PON AQUI LA EXTENSION DONDE QUIERES QUE SUENE

if ($apikey == "") {
    header($_SERVER["SERVER_PROTOCOL"]." 404 Not Found", true, 404);
    echo "Falta especificar el apikey, edita el fichero PHP y complete la variable apikey con el apikey correspondiente.";
    die();
} else if ($origin == "") {
    header($_SERVER["SERVER_PROTOCOL"]." 404 Not Found", true, 404);
    echo "Falta especificar la extension de origen, edita el fichero PHP y complete la variable apikey con el apikey correspondiente.";
    die();
} else {
    $opts = array(
       'http' => array(
           'method' => "GET",
           'header' => "Content-type: application/json\n"
                       ."X-Api-Key: ".$apikey,
       )
    );

    $context = stream_context_create($opts);
    $response = file_get_contents("https://vpbx.me/api/originatecall/".$origin."/".$_POST['number'], false, $context);

    //echo $response;
    echo "llamando...";
}
?>