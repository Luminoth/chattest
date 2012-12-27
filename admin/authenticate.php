<?
    $tag = "<error>Unknown error</error>";
    if(empty($_POST['username']))
        $tag = "<error>You must supply a username</error>";
    else if(empty($_POST['password']))
        $tag = "<error>You must supply a password</error>";
    else {
        include('database.inc');

        $conn = db_connect();
        if($conn) {
            $username = $_POST['username'];
            $passwordmd5 = md5($_POST['password']);

            $query = "select * from accounts where username='$username' and passwordmd5='$passwordmd5'";
            $result = mysql_query($query, $conn);
            $count = mysql_num_rows($result);
            if($count > 0) {
                $valid = mysql_result($result, 0, 'valid');
                $administrator = mysql_result($result, 0, 'administrator');
                $tag = strcasecmp($valid, "Y") && strcasecmp($administrator, "Y")
                    ? "<error>You don't have administrator rights</error>"
                    : "<success>Authentication successful</success>";
            } else {
                $tag = "<error>Invalid username or password</error>";
            }
        } else {
            $tag = "<error>Database Error</error>";
        }
    }

    header('Content-Type: text/xml');
?>

<authenticate>
    <? print $tag ?>
</authenticate>
