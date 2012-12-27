<?
function db_connect()
{
    $result = mysql_pconnect('localhost', 'root', 'mysqlownz');
    if(!$result) return false;

    if(!mysql_select_db('chattest'))
        return false;

    return $result;
}
?>
