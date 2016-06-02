<?php

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
					
				</AssetList>
				<LiabilityList/>
				<AddressList>
					<ApplicationAddressCanada key="MainCurrentAddKey1" cityTown="Address" provinceCode="20" postalCode="T6G-8H9" countryCode="1">
                                                <PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="Address" streetType="-1" streetDirection="-1" POBoxRRNumber=""/>
                                          </ApplicationAddressCanada>
				</AddressList>
			</CommonData>
			<CustomerData>
				<CustomerList>
					<CustomerBorrower key="MainCustomerKey1" dateBirth="1980-10-16" lastName="Pallister3" firstName="Guy" emailAddress1="guy@syml.ca" maritalStatus="1" numberOfDependents="0">
                                                                                <EmploymentList>
                                                                                    <Employment employmentType="1" employmentStatus="10" dateStart="2008-03-30" jobTitle="Commercial Technician / Installer" companyName="Chubb Security">
                                                                                        <EarnedIncomeList>
                                                                                            <EarnedIncome earnedIncomeType="1" paymentFrequency="12" earnedIncomeAmount="4145.00"/>
                                                                                        </EarnedIncomeList>
                                                                                    </Employment>
                                                                                </EmploymentList>
                                                                         </CustomerBorrower>
				</CustomerList>
				<CustomerAddressList>
					<CustomerAddressPrimaryResidence fromDate="2008-03-30" refkeyAddress="MainCurrentAddKey1">
                                                                       <CustomerReference refkeyCustomer="MainCustomerKey1"/><AddressOccupancyOwnerOccupied refkeyAsset= "AssetPrimaryRealEstate1"/>
                                        </CustomerAddressPrimaryResidence>
				</CustomerAddressList>
				<CustomerAssetList>
					
				</CustomerAssetList>
				<CustomerLiabilityList/>
			</CustomerData>
			<MortgageApplication agentUserId="0">
				<SubjectPropertyList>
					 <SubjectProperty  parkingType="3" yearBuilt="1999" propertyDescriptionType="7"  heatingType="2" waterSupplyType="10" waterWasteType="10" MLSNumber="0000">
                                            <SubjectPropertyOccupancyOwnerOccupied/>

                                            <LegalAddress details="None" levelNumber="0000" lotNumber="0000" PIN="0000" planNumber="0000" unitNumber="0000"/>

                                            <Condo annualCondoFees="0000"/>

                                            <PropertyTax annualTaxAmount="5555.0"/>
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