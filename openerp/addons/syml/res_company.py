import hashlib
from osv import fields,osv


class res_company(osv.osv):
    _inherit = 'res.company'

#    def create(self, cr, uid, values, context=None):
#        newid = super(res_company, self).create(cr, uid, values, context)
#        print "values>>>>",values
#        return newid


#    def write(self, cr, uid, ids, vals, context=None):
#        res = {}
#        print "valsss>>>",vals
#        if vals:
#            newid = super(res_company, self).write(cr, uid, ids, vals, context)
#            if newid:
#                print "new_iddd>>",ids
#                self_brw = self.browse(cr, uid, ids[0])
#                db_name = self_brw.db_name
#                #user_name = self_brw.user_name
#                #password = self_brw.password
#                m = hashlib.md5()
#                print "db_name>>",db_name
#                #print "user_name>>",user_name
#                #print "password>>",password
#                m.update(db_name)
#                md5_db_name = m.digest()
#                #unicode_val = md5_db_name.unicode('utf-8')
#                #unicode_val = unicode(md5_db_name, 'utf-8')
#                #md5_user_name =  m.update(user_name).hexdigest()
#                #md5_password =  m.update(password).hexdigest()
#                #print "unicode_val>>>>>",unicode_val
#                res['db_name'] = md5_db_name
#
#        return res

    _columns={
        'morweb_request':fields.text('Moreweb Request'),
        'visdom_url':fields.char('Visdom URL',size=240),
        'db_name':fields.char('Database Name',size=128),
        'user_name':fields.char('User Name',size=128),
        'password':fields.char('Password',size=128),
#  UW App
        'uw_desiredProduct':fields.char('Desired Product',size=128, help="takes Opportunity ID as parameter"),
        'uw_allProduct':fields.char('All Product',size=128, help="takes Opportunity ID as parameter"),
        'uw_postSelection':fields.char('Post Selection',size=128, help="takes Opportunity ID and Product ID as parameter"),
        'uw_finalVerify':fields.char('Final Verify',size=128, help="takes Opportunity ID and Product ID as parameter"),
        'uw_product':fields.char('Product',size=128, help="takes Opportunity ID as parameter"),
        'uw_lender':fields.char('Lender',size=128, help="takes Opportunity ID as parameter"),
	'bookeeper_email':fields.char('Bookeeper Email',size=256),
        'bookeeper_name':fields.char('Bookeeper Name',size=256),
    }
    _defaults={
        'morweb_request':'''<?php


error_reporting(E_ALL);
ini_set("display_errors", 1);

date_default_timezone_set('UTC');

/*
	To test BDI submission, modify the 4 variables below:
		- $bdi_url
		- $soap_user
		- $soap_pass
		- $data
*/

$bdi_url = "https://uat.services.morweb.ca:4430/mscis/MSC_IntegrationService_MSCISOrchestration_MSCReceive_Port.asmx";
$soap_user = "VisdomTest";
$soap_pass = "T3mvP23G";
$data = <<<EOD
	<ProcessRequest xmlns="http://tempuri.org/">
		<clipboard xmlns="http://mscanada.com">
			<context applicationName="BDIB2B" userid="VisdomTest" language="en-CA" dateTime="2010-07-14T11:42:04"/>
			<msgRequest requestId="123" serviceType="BrokerDataIngest" source="VisdomVTDev" provider="MorWEBTraining" recipient="MorWEB">
			</msgRequest>
			<applicationData>

				<BDIRequest createdUserId="sbandarkar" createdUnitId="MSC-2" createdDateTime="2012-02-24T16:43:55" xsi:schemaLocation="http://MSC.IntegrationService.Schemas.MorWEB.BDI.Request.1MSCIS_BDI_Request_V1.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://MSC.IntegrationService.Schemas.MorWEB.BDI.Request.1" xmlns:b="http://schemas.microsoft.com/BizTalk/2003" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			<CommonData>
				<AssetList>
					<AssetRealEstate value="0.00" key="AssetPrimaryRealEstate1"/>
				        'visdom_url':fields.char('Visdom URL',size=240),
#        'db_name':fields.char('Database Name',size=128),
#        'user_name':fields.char('User Name',size=128),
#        'password':fields.char('Password',size=128),	<AssetOther key="AssetSavingkey1" value="10200.00" assetType="99" description="Other"/>
				</AssetList>
				<LiabilityList/>
				<AddressList>
<ApplicationAddressCanada key="MainCurrentAddKey1" cityTown="" provinceCode="10" postalCode="V2A1A5" countryCode="1">
<PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="" streetType="-1" streetDirection="-1" POBoxRRNumber=""/>
					</ApplicationAddressCanada>
					<ApplicationAddressCanada key="MainCurrentAddKey2" cityTown="- " provinceCode="10" postalCode="M1M1M1" countryCode="1">
						<PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="-" streetType="-1" streetDirection="-1" POBoxRRNumber=""/>
					</ApplicationAddressCanada>
<ApplicationAddressCanada key="MainCurrentAddKey3" cityTown=" , " provinceCode="10" postalCode="M1M1M1" countryCode="1">
						<PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="-" streetType="-1" streetDirection="-1" POBoxRRNumber=""/>
					</ApplicationAddressCanada>
				</AddressList>
			</CommonData>
			<CustomerData>
				<CustomerList>
<CustomerBorrower key="MainCustomerKey1" honorific="1" lastName="THakur" firstName="ankit.thakur@bistasolutions." emailAddress1="ankit.thakur@bistasolutions." maritalStatus="1" dateBirth="1984-11-14" numberOfDependents="">
						<EmploymentList>
<Employment employmentType="1" employmentStatus="10" dateStart="2008-03-30" jobTitle="" companyName="bistasolutions">
								<EarnedIncomeList>
									<EarnedIncome earnedIncomeType="1" paymentFrequency="12" earnedIncomeAmount="4145.00"/>
								</EarnedIncomeList>
							</Employment>
						</EmploymentList>
					</CustomerBorrower>
				</CustomerList>
				<CustomerAddressList>
					<CustomerAddressPrimaryResidence fromDate="2008-03-30" refkeyAddress="MainCurrentAddKey1">
						<CustomerReference refkeyCustomer="MainCustomerKey1"/>
						<AddressOccupancyOwnerOccupied refkeyAsset="AssetPrimaryRealEstate1"/>
					</CustomerAddressPrimaryResidence>
				</CustomerAddressList>
				<CustomerAssetList>
					<CustomerAssetOther refkeyAsset="AssetSavingkey1">
						<CustomerReference refkeyCustomer="MainCustomerKey1"/>
					</CustomerAssetOther>
				</CustomerAssetList>
				<CustomerLiabilityList/>
			</CustomerData>
			<MortgageApplication agentUserId="0">
				<SubjectPropertyList>
					<SubjectProperty occupancyPurpose="1" parkingType="7" yearBuilt="1999" propertyDescriptionType="1">
						<SubjectPropertyOccupancyOwnerOccupied/>
						<LegalAddress/>
						<Freehold/>db
						<PropertyTax annualTaxAmount="2000.00"/>
						<PropertyAppraisal/>
						<SubjectPropertyAddress refkeyAddress="MainCurrentAddKey2"/>
					</SubjectProperty>
				</SubjectPropertyList>
				<LoanList>
					<Loan loanAmount="0.00" chargeType="1"/>
				</LoanList>
			</MortgageApplication>
		</BDIRequest>

			</applicationData>
		</clipboard>
	</ProcessRequest>
EOD;

send($soap_user, $soap_pass, $bdi_url, $data);

/* ---------------------------------- */

function send($user, $pass, $bdi_url, $data) {
	$timestamp = date ("YmdHi");
	$time = date ("Y-m-d\\TH:i:s\Z");

	echo sprintf("<b>%-20s :</b> %s", "User", $user) . "<br>";
	echo sprintf("<b>%-20s :</b> %s", "Password", $pass) . "<br>";
	echo sprintf("<b>%-20s :</b> %s", "Timestamp", $time) . "<br>";
	echo sprintf("<b>%-20s :</b> %s", "Timestamp", $timestamp) . "<br>";

	echo "<br>";

	$request = create_soap_envelope($user, create_password_hash($timestamp, $pass), create_time_nonce($timestamp), $time, $data);
	$response = send_request($request, $bdi_url);

	echo "<b>Request (SOAP Envolope) : </b><br><pre><code class=\"xml\">" . xmlpp($request) . "</code></pre><br><br>";
	echo "<b>Response : </b><br><pre><code class=\"xml\">" . xmlpp($response) . "</code></pre><br><br>";
}

function create_password_hash($timestamp, $pass) {
	$hash = base64_encode(sha1($timestamp . "&" . $pass, true));
	echo sprintf("<b>%-20s :</b> %s", "Hash", $hash) . "<br>";
	return $hash;
}

function create_time_nonce($timestamp) {
	$nonce = base64_encode(sha1($timestamp, true));
	echo sprintf("<b>%-20s :</b> %s", "Nonce", $nonce) . "<br>";
	return $nonce;
}

function create_soap_envelope($username, $password, $nonce, $time, $data) {
	echo "<br>";

	// Load XML document
	$xml = new SimpleXMLElement($data);
	$body = substr($xml->asXML(), strpos($xml->asXML(), "?>") + 2);

	// Wrap data in SOAP Envelope
	$data = "
		<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:wsa=\"http://schemas.xmlsoap.org/ws/2004/03/addressing\" xmlns:wsse=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\" xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">
			<soap:Header />
			<soap:Body>
				$body
			</soap:Body>
		</soap:Envelope>
	";

	$soap = new SimpleXMLElement($data);

	// Add WS-Security into the header
	$node = $soap->xpath("//*[local-name()='Header']");

	if ($node) {
		// Add Security node
		$security = $node[0]->addChild('wsse:Security', null, 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd');
		$security->addAttribute('wsse:mustUnderstand', '1', 'http://schemas.xmlsoap.org/soap/envelope/');

		// Add UsernameToken node
		$node = $security->addChild('wsse:UsernameToken');
		$node->addChild('wsse:Username', $username);
		$node->addChild('wsse:Nonce', $nonce);
		$node->addChild('wsu:Created', $time, 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd');

		// Add Password node
		$node = $node->addChild('wsse:Password', $password);
		$node->addAttribute('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText');
	} else {
		return 0;
	}

	return $soap->asXML();
}

function xmlpp($data) {

	$xml = new SimpleXMLElement($data);

	$dom = new DOMDocument('1.0');
	$dom->preserveWhiteSpace = false;
	$dom->formatOutput = true;
	$dom->loadXML($xml->asXML());

	return htmlentities($dom->saveXML());
}

function send_request($xml, $bdi_url) {
	$header = array(	"Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
					"Content-type: text/xml; charset=utf-8",
					"Cache-Control: max-age=0",
					"Connection: keep-alive",
					"Keep-Alive: 300",
					"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7",
					"Accept-Language: en-us,en;q=0.5",
					"SOAPAction:http://tempuri.org/MSC_IntegrationService_MSCISOrchestration_MSCReceive_Port/ProcessRequest");

	$c = curl_init();

	curl_setopt($c, CURLOPT_USERAGENT, "MEdge");
	curl_setopt($c, CURLOPT_URL, $bdi_url);
	curl_setopt($c, CURLOPT_TIMEOUT, 900);
	curl_setopt($c, CURLOPT_SSL_VERIFYPEER, FALSE);
	curl_setopt($c, CURLOPT_RETURNTRANSFER, TRUE);
	curl_setopt($c, CURLOPT_HTTPHEADER, $header);
	curl_setopt($c, CURLOPT_POST, 1);
	curl_setopt($c, CURLOPT_POSTFIELDS, $xml);

	$resp = array('xml' => curl_exec ($c), 'error' => curl_error ($c));

	curl_close ($c);

	return $resp['xml'];
}

?>
                  ?>
'''

    }
res_company()
