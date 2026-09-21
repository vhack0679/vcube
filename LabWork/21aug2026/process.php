<?php
/**
 * Secure Form Processor for Vijaya Homoeopathic
 *
 * This script handles form submissions from the React frontend.
 *
 * It performs:
 * 1. Secure JSON-only communication.
 * 2. Server-side reCAPTCHA verification.
 * 3. Strict server-side validation of ALL inputs (text, email, phone, file).
 * 4. XSS protection by escaping ALL user input before use.
 * 5. Secure file upload handling (checking type, size).
 * 6. Secure email sending with PHPMailer.
 * 7. Proper error handling and logging.
 */

// --- PHPMailer Imports ---
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

// --- UPDATED: Use relative path to go UP one level from /App/ to the root ---
require '../PHPMailer/PHPMailer/PHPMailer.php';
require '../PHPMailer/PHPMailer/Exception.php';
require '../PHPMailer/PHPMailer/SMTP.php';

// --- Configuration ---
// !! IMPORTANT: For better security, move this to a `config.php` file 
//    that is OUTSIDE your public web directory (e.g., in a folder above public_html)
//    and then use: require_once '/path/to/your/config.php';
$config = [
    'recaptcha_secret' => '6LePXZYtAAAAAI-5bxn4hhL0D2JMxKLZFeV6kiNZ', // Your reCAPTCHA secret key
    'smtp_host'        => 'smtp.gmail.com',
    'smtp_username'    => 'vijayahomoeopathic@gmail.com',
    'smtp_password'    => 'vrizhiwlhrnimqas', // Your App Password
    'smtp_port'        => 587,
    'smtp_secure'      => PHPMailer::ENCRYPTION_STARTTLS,
    'clinic_email'     => 'vijayahomoeopathic@gmail.com', // Email to receive submissions
    'clinic_name'      => 'Vijaya Homoeopathic Clinic'
];

// --- Security Validation Constants ---
define('MAX_FILE_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_FILE_TYPES', [
    'image/jpeg' => 'jpg',
    'image/png'  => 'png',
    'image/webp' => 'webp'
]);

// --- Helper Functions ---

/**
 * Sends a JSON error response and exits the script.
 * @param string $message The error message to send.
 * @param int $statusCode The HTTP status code (e.g., 400 for bad request).
 */
function sendError($message, $statusCode = 400) {
    http_response_code($statusCode);
    echo json_encode(['success' => false, 'error' => $message]);
    exit;
}

/**
 * Sends a JSON success response and exits the script.
 * @param array $data Optional data to include in the response.
 */
function sendSuccess($data = []) {
    echo json_encode(array_merge(['success' => true], $data));
    exit;
}

/**
 * Sanitizes a string for safe HTML output.
 * @param string $data The input string.
 * @return string The sanitized string.
 */
function sanitize($data) {
    return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
}

/** Build a consistent, responsive email shell for clinic messages. */
function emailShell($content, $clinicName, $logoCid = '') {
    $logo = $logoCid
        ? "<img src='cid:{$logoCid}' alt='" . htmlspecialchars($clinicName, ENT_QUOTES, 'UTF-8') . " logo' style='display:block;width:56px;height:56px;object-fit:contain;margin:0 auto 10px;'>"
        : '';

    return "<!doctype html>
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <style>
      body{margin:0;padding:0;background:#f5f4fa;color:#28224b;font-family:Arial,Helvetica,sans-serif}
      .wrap{width:100%;padding:28px 12px;box-sizing:border-box}.card{max-width:680px;margin:0 auto;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 10px 28px rgba(47,37,107,.12)}
      .hero{padding:24px 28px 22px;background:linear-gradient(135deg,#ffffff 0%,#f7f5ff 100%);border-top:6px solid #28206a;border-bottom:3px solid #df1d2f;color:#28206a;text-align:center}.hero img{width:84px!important;height:84px!important;margin-bottom:8px!important}.hero h1{margin:0;font-size:24px;line-height:1.25;color:#28206a}.hero p{margin:7px 0 0;color:#b51b2a;font-size:14px;font-weight:bold}
      .body{padding:28px}.eyebrow{margin:0 0 8px;color:#b51b2a;font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase}.title{margin:0 0 14px;font-size:24px;line-height:1.3;color:#28206a}.copy{margin:0 0 16px;line-height:1.65;color:#514b70}
      .info{width:100%;border-collapse:separate;border-spacing:0 8px}.info td{padding:12px 14px;background:#f7f6fc;vertical-align:top;line-height:1.45}.info td:first-child{width:34%;border-radius:9px 0 0 9px;color:#28206a;font-weight:bold}.info td:last-child{border-radius:0 9px 9px 0;color:#3f395d;word-break:break-word}
      .photo{display:block;width:100%;max-width:360px;max-height:300px;object-fit:cover;margin:18px auto 0;border:1px solid #ddd9ee;border-radius:12px}.json{margin:16px 0 0;padding:14px;background:#211c43;border-radius:11px;color:#f3efff;font:12px/1.5 Consolas,Monaco,monospace;white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere}.json-note{margin:8px 0 0;color:#766f92;font-size:12px;line-height:1.5}
      .footer{padding:18px 28px;background:#f1eff9;text-align:center;color:#716b8b;font-size:12px;line-height:1.5}
      @media only screen and (max-width:520px){.wrap{padding:0}.card{border-radius:0;box-shadow:none}.hero{padding:24px 18px}.body{padding:22px 16px}.info td{display:block;width:auto!important;border-radius:8px!important}.info td:first-child{padding-bottom:4px}.info td:last-child{padding-top:5px;margin-top:-8px}.footer{padding:16px}}
    </style></head><body><div class='wrap'><div class='card'>
      <div class='hero'>{$logo}<h1>{$clinicName}</h1><p>Online Consultation Care</p></div>
      <div class='body'>{$content}</div>
      <div class='footer'>This is an automated message from {$clinicName}. Please do not share it publicly.</div>
    </div></div></body></html>";
}

function infoRows($data) {
    $fields = [
        'Full name' => $data['name'] . ' ' . $data['SurName'], 'Gender' => ucfirst($data['gender']),
        'Age' => $data['age'], 'Occupation' => $data['occupation'], 'Address' => nl2br($data['address']),
        'Phone' => $data['phone'], 'Email' => $data['email_sanitized']
    ];
    $rows = '';
    foreach ($fields as $label => $value) {
        $rows .= "<tr><td>{$label}</td><td>{$value}</td></tr>";
    }
    return $rows;
}

// --- Main Script Execution ---

// 1. Set global headers and error logging
header('Content-Type: application/json'); // MUST output JSON
error_reporting(0); // Turn off error display to users
ini_set('display_errors', 0);
ini_set('log_errors', 1); // Log errors to the server's error log
// ini_set('error_log', '/path/to/your/php-error.log'); // Optional: specify a log file

// 2. Check Request Method
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendError('Invalid request method.', 405);
}

// 3. Verify reCAPTCHA
$recaptcha_token = isset($_POST['recaptcha_token']) ? $_POST['recaptcha_token'] : '';
if (empty($recaptcha_token)) {
    sendError('reCAPTCHA token is missing.');
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://www.google.com/recaptcha/api/siteverify");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
    'secret'   => $config['recaptcha_secret'],
    'response' => $recaptcha_token,
    'remoteip' => $_SERVER['REMOTE_ADDR']
]));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);
$responseKeys = json_decode($response, true);

if (!$responseKeys || !$responseKeys['success']) {
    // Log the actual reCAPTCHA error for debugging
    error_log('reCAPTCHA verification failed: ' . json_encode($responseKeys['error-codes'] ?? 'Unknown error'));
    sendError('reCAPTCHA verification failed. Please try again.');
}

// 4. Server-Side Data Validation & Sanitization
$errors = [];
$data = [];

// Name
$data['name'] = isset($_POST['name']) ? sanitize($_POST['name']) : '';
if (empty($data['name']) || strlen($data['name']) > 100 || !preg_match("/^[A-Za-z\s\-'.]+$/", $data['name'])) {
    $errors[] = 'Invalid name.';
}

// Surname
$data['SurName'] = isset($_POST['SurName']) ? sanitize($_POST['SurName']) : '';
if (empty($data['SurName']) || strlen($data['SurName']) > 100 || !preg_match("/^[A-Za-z\s\-'.]+$/", $data['SurName'])) {
    $errors[] = 'Invalid surname.';
}

// Gender
$data['gender'] = isset($_POST['gender']) ? sanitize($_POST['gender']) : '';
if (empty($data['gender']) || !in_array($data['gender'], ['male', 'female', 'other'])) {
    $errors[] = 'Invalid gender.';
}

// Age
$data['age'] = isset($_POST['age']) ? filter_var($_POST['age'], FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 120]]) : false;
if ($data['age'] === false) {
    $errors[] = 'Invalid age. Must be between 1 and 120.';
}

// Occupation
$data['occupation'] = isset($_POST['occupation']) ? sanitize($_POST['occupation']) : '';
if (empty($data['occupation']) || strlen($data['occupation']) > 100) {
    $errors[] = 'Invalid occupation. Max 100 characters.';
}

// Address
$data['address'] = isset($_POST['address']) ? sanitize($_POST['address']) : '';
if (empty($data['address']) || strlen($data['address']) > 500) {
    $errors[] = 'Invalid address. Max 500 characters.';
}

// Phone
$data['phone'] = isset($_POST['phone']) ? sanitize($_POST['phone']) : '';
if (empty($data['phone']) || !preg_match("/^\+[1-9][0-9]{7,14}$/", $data['phone'])) {
    $errors[] = 'Invalid phone number. Must be in +[countrycode][number] format.';
}

// Email
$data['email'] = isset($_POST['email']) ? trim($_POST['email']) : '';
if (empty($data['email']) || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Invalid email address.';
}
$data['email_sanitized'] = sanitize($data['email']); // Sanitized version for HTML body

// Symptoms
$data['symptoms'] = isset($_POST['symptoms']) ? sanitize($_POST['symptoms']) : '';
if (empty($data['symptoms']) || strlen($data['symptoms']) > 1000) {
    $errors[] = 'Invalid symptoms. Max 1000 characters.';
}

// 5. Server-Side File Validation
$fileTmpPath = '';
$fileName = '';

if (!isset($_FILES['photo']) || $_FILES['photo']['error'] !== UPLOAD_ERR_OK) {
    $errors[] = 'File upload error. Please select a photo.';
} else {
    $fileTmpPath = $_FILES['photo']['tmp_name'];
    $fileName    = sanitize($_FILES['photo']['name']);
    $fileSize    = $_FILES['photo']['size'];
    
    // Check size
    if ($fileSize > MAX_FILE_SIZE) {
        $errors[] = 'File is too large. Max 5MB allowed.';
    }

    // Check MIME type
    $mimeType = mime_content_type($fileTmpPath);
    if (!array_key_exists($mimeType, ALLOWED_FILE_TYPES)) {
        $errors[] = 'Invalid file type. Only JPG, PNG, and WEBP are allowed.';
    }
}

// If there are any validation errors, send them all at once
if (!empty($errors)) {
    sendError(implode(' ', $errors));
}

// Keep the validated photo in the structured submission as requested.
$photoBase64 = base64_encode(file_get_contents($fileTmpPath));
$logoPath = __DIR__ . DIRECTORY_SEPARATOR . 'onlylogo.png';

// --- 6. Send Emails ---
$mail = new PHPMailer(true);

try {
    // Server settings
    $mail->SMTPDebug = SMTP::DEBUG_OFF; // Turn off debug output for production
    $mail->isSMTP();
    $mail->Host       = $config['smtp_host'];
    $mail->SMTPAuth   = true;
    $mail->Username   = $config['smtp_username'];
    $mail->Password   = $config['smtp_password'];
    $mail->SMTPSecure = $config['smtp_secure'];
    $mail->Port       = $config['smtp_port'];

    // --- Email to Clinic ---
    // Note: SetFrom MUST be the same as the Username (smtp_username) to avoid spam filters
    $mail->setFrom($config['smtp_username'], $config['clinic_name']);
    $mail->addAddress($config['clinic_email']);
    $mail->addReplyTo($data['email'], $data['name']); // Add patient as "Reply-To"

    // Content for the main email
    $mail->isHTML(true);
    $mail->Subject = 'New Online Consultation Request from ' . $data['name'];
    
    $patientJsonData = [
        'name'       => $data['name'],
        'surname'    => $data['SurName'],
        'gender'     => $data['gender'],
        'age'        => $data['age'],
        'occupation' => $data['occupation'],
        'address'    => $data['address'],
        'phone'      => $data['phone'],
        'email'      => $data['email'],
        'symptoms'   => $data['symptoms'],
        'photo'      => $photoBase64
    ];
    $patientJson = json_encode($patientJsonData, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    $patientJsonHtml = htmlspecialchars($patientJson, ENT_QUOTES, 'UTF-8');

    $logoCid = '';
    if (is_readable($logoPath)) {
        $logoCid = 'clinic-logo';
        $mail->addEmbeddedImage($logoPath, $logoCid, 'onlylogo.png', 'base64', 'image/png');
    }
    $mail->addEmbeddedImage($fileTmpPath, 'patient-photo', $fileName, 'base64', $mimeType);
    $adminContent = "
        <p class='eyebrow'>New submission</p>
        <h2 class='title'>Patient consultation request</h2>
        <p class='copy'>A new online consultation request has been received. Use the contact details below to follow up with the patient.</p>
        <table class='info' role='presentation'>" . infoRows($data) . "</table>
        <p class='eyebrow' style='margin-top:22px;'>Reported symptoms</p>
        <p class='copy'>" . nl2br($data['symptoms']) . "</p>
        <p class='eyebrow' style='margin-top:22px;'>Uploaded photo</p>
        <img class='photo' src='cid:patient-photo' alt='Patient uploaded photo'>
        <p class='eyebrow' style='margin-top:24px;'>Patient data (JSON)</p>
        <pre class='json'>{$patientJsonHtml}</pre>
        <p class='json-note'>To copy or save the complete JSON, open the attached <strong>patient-data.json</strong> file.</p>";
    $mail->Body = emailShell($adminContent, $config['clinic_name'], $logoCid);

    // Keep the original as a downloadable attachment too.
    $mail->addAttachment($fileTmpPath, $fileName);
    $mail->addStringAttachment($patientJson, 'patient-data.json', PHPMailer::ENCODING_BASE64, 'application/json');
    
    $mail->send();

    // --- Confirmation Email to User ---
    $mail->clearAddresses();
    $mail->clearAttachments();
    $mail->clearReplyTos();

    $mail->addAddress($data['email']); // Send to the patient's email
    $mail->Subject = 'Consultation Request Received - Vijaya Homoeopathic Clinic';
    $logoCid = '';
    if (is_readable($logoPath)) {
        $logoCid = 'clinic-logo';
        $mail->addEmbeddedImage($logoPath, $logoCid, 'onlylogo.png', 'base64', 'image/png');
    }
    $mail->addEmbeddedImage($fileTmpPath, 'patient-photo', $fileName, 'base64', $mimeType);
    $clientContent = "
        <p class='eyebrow'>Request received</p>
        <h2 class='title'>Thank you, {$data['name']}!</h2>
        <p class='copy'>We have successfully received your online consultation request. Dr. Bomma Bhaskar or Dr. Bomma Ravi will review your information and contact you shortly.</p>
        <p class='copy'>Your health is our priority. Here is a preview of the photo included with your request.</p>
        <img class='photo' src='cid:patient-photo' alt='Your uploaded photo'>
        <p class='copy' style='margin-top:22px;'>Best regards,<br><strong>{$config['clinic_name']}</strong></p>";
    $mail->Body = emailShell($clientContent, $config['clinic_name'], $logoCid);
    $mail->send();

    // 7. Send final success response to frontend
    sendSuccess();

} catch (Exception $e) {
    // Log the detailed error and send a generic message to the user
    error_log('PHPMailer Error: ' . $mail->ErrorInfo);
    sendError('Message could not be sent. Please try again later.', 500);
}
?>
