<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Chattest Administration</title>
    <link href="css/admin.css" rel="stylesheet" type="text/css" />
    <script src="js/admin.js" type="text/javascript"></script>
    <script src="js/ajax.js" type="text/javascript"></script>
</head>
<body>

<table cellspacing="0" cellpadding="3" border="1">
<tr>
    <td colspan="7">Chattest Users</td>
</tr>
<tr>
    <td>Id</td>
    <td>Username</td>
    <td>Password MD5</td>
    <td>Currently Logged In</td>
    <td>Can Login</td>
    <td>Valid Account</td>
    <td>Administrator</td>
</tr>
<?
    include('database.inc');

    $conn = db_connect();
    if($conn) {
        $query = "select * from accounts order by id";
        $result = mysql_query($query, $conn);
        $count = mysql_num_rows($result);
        while($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
?>
<tr>
<?
            foreach($row as $column) {
?>
    <td><? print $column ?></td>
<?
            }
?>
</tr>
<?
        }
    }
?>
</table>

<div><a href="logout.html">Logout</a></div>

</body>
</html>
