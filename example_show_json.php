<HTML>
<BODY>
<TABLE BORDER='1'>
<TR><TH>sequence</TH><TH>data</TH></TR>
<?
	$handle = popen('./httping -c 3 www.google.com -F -M', 'r');
	$read = '';
	while($line = fgets($handle))
		$read .= ' '.$line;
	fclose($handle);

	$fields = json_decode($read);

	for($index=0; $index<count($fields); $index++)
	{
		?><TR><?
		?><TD><? print $index + 1; ?></TD><?
		?><TD><? ?></TD><?
		?></TR><?

		?><TR><?
		?><TD><? ?></TD><?
		?><TD><?
			?><TABLE><?
			?><TR><TH>key</TH><TH>value</TH></TR><?
			foreach($fields[$index] as $key => $value)
			{
				?><TR><?
				?><TD><? print $key; ?></TD><?
				?><TD><? print $value; ?></TD><?
				?></TR><?
			}
			?></TABLE><?
		?></TD><?
		?></TR><?
	}
?>
</TABLE>
</BODY>
</HTML>
