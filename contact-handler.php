<?php
/**
 * Contact Form Handler
 * Clear Choice Restoration
 *
 * Processes contact form submissions and sends email notifications
 */

header('Content-Type: application/json');

// Configuration
$config = [
    'to_email' => 'info@ccrroof.com',
    'from_email' => 'noreply@ccrroof.com',
    'company_name' => 'Clear Choice Restoration',
    'site_url' => 'https://ccrroof.com'
];

/**
 * Sanitize input data
 */
function sanitize($input) {
    return htmlspecialchars(strip_tags(trim($input)), ENT_QUOTES, 'UTF-8');
}

/**
 * Validate email address
 */
function isValidEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Validate phone number (basic validation)
 */
function isValidPhone($phone) {
    $digits = preg_replace('/\D/', '', $phone);
    return strlen($digits) >= 10 && strlen($digits) <= 15;
}

/**
 * Send email notification
 */
function sendEmail($to, $subject, $htmlBody, $textBody, $replyTo, $fromEmail, $fromName) {
    $boundary = md5(time());

    $headers = [
        'From: ' . $fromName . ' <' . $fromEmail . '>',
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
        'X-Mailer: PHP/' . phpversion()
    ];

    $body = "--{$boundary}\r\n";
    $body .= "Content-Type: text/plain; charset=UTF-8\r\n\r\n";
    $body .= $textBody . "\r\n\r\n";
    $body .= "--{$boundary}\r\n";
    $body .= "Content-Type: text/html; charset=UTF-8\r\n\r\n";
    $body .= $htmlBody . "\r\n\r\n";
    $body .= "--{$boundary}--";

    return mail($to, $subject, $body, implode("\r\n", $headers));
}

/**
 * Log submission for backup
 */
function logSubmission($data) {
    $logDir = __DIR__ . '/logs';
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }

    $logFile = $logDir . '/contact_' . date('Y-m') . '.log';
    $logEntry = date('Y-m-d H:i:s') . ' | ' . json_encode($data) . "\n";

    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit();
}

// Honeypot check (if a hidden field was filled, it's likely spam)
if (!empty($_POST['website'])) {
    // Silently accept but don't process
    echo json_encode(['success' => true]);
    exit();
}

// Collect and sanitize form data
$formData = [
    'first_name' => sanitize($_POST['first_name'] ?? ''),
    'last_name' => sanitize($_POST['last_name'] ?? ''),
    'email' => sanitize($_POST['email'] ?? ''),
    'phone' => sanitize($_POST['phone'] ?? ''),
    'address' => sanitize($_POST['address'] ?? ''),
    'service' => sanitize($_POST['service'] ?? ''),
    'urgency' => sanitize($_POST['urgency'] ?? 'normal'),
    'message' => sanitize($_POST['message'] ?? ''),
    'insurance' => isset($_POST['insurance']) ? 'Yes' : 'No',
    'submitted_at' => date('Y-m-d H:i:s'),
    'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'Unknown',
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown'
];

// Validation
$errors = [];

if (empty($formData['first_name'])) {
    $errors[] = 'First name is required';
}

if (empty($formData['last_name'])) {
    $errors[] = 'Last name is required';
}

if (empty($formData['email']) || !isValidEmail($formData['email'])) {
    $errors[] = 'Valid email is required';
}

if (empty($formData['phone']) || !isValidPhone($formData['phone'])) {
    $errors[] = 'Valid phone number is required';
}

if (empty($formData['service'])) {
    $errors[] = 'Please select a service';
}

// Check for rate limiting (simple implementation)
$rateFile = __DIR__ . '/logs/rate_' . md5($_SERVER['REMOTE_ADDR']) . '.txt';
if (file_exists($rateFile)) {
    $lastSubmit = (int) file_get_contents($rateFile);
    if (time() - $lastSubmit < 60) { // 1 minute between submissions
        $errors[] = 'Please wait before submitting again';
    }
}

// Return errors if any
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => implode('. ', $errors), 'errors' => $errors]);
    exit();
}

// Log submission
logSubmission($formData);

// Update rate limit file
$rateDir = dirname($rateFile);
if (!is_dir($rateDir)) {
    mkdir($rateDir, 0755, true);
}
file_put_contents($rateFile, time());

// Service labels
$serviceLabels = [
    'roof-inspection' => 'Free Roof Inspection',
    'hail-damage' => 'Hail/Storm Damage Assessment',
    'roof-replacement' => 'Roof Replacement',
    'roof-repair' => 'Roof Repair',
    'gutter-services' => 'Gutter Services',
    'siding' => 'Siding Installation/Repair',
    'water-damage' => 'Water Damage/Mitigation',
    'insurance-claim' => 'Insurance Claim Assistance',
    'other' => 'Other'
];

$serviceLabel = $serviceLabels[$formData['service']] ?? $formData['service'];

// Urgency labels
$urgencyLabels = [
    'normal' => 'Normal - Schedule at convenience',
    'soon' => 'Soon - Within the next week',
    'urgent' => 'Urgent - Active leak or damage',
    'emergency' => 'EMERGENCY - Needs immediate attention'
];

$urgencyLabel = $urgencyLabels[$formData['urgency']] ?? $formData['urgency'];
$isUrgent = in_array($formData['urgency'], ['urgent', 'emergency']);

// Build email content
$fullName = $formData['first_name'] . ' ' . $formData['last_name'];

$subject = ($isUrgent ? '[URGENT] ' : '') . 'New Contact Form Submission - ' . $serviceLabel;

$htmlBody = '
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #1B4B8F; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .field { margin-bottom: 15px; }
        .label { font-weight: bold; color: #1B4B8F; }
        .value { margin-top: 5px; }
        .urgent { background: #ffebee; border-left: 4px solid #c44536; padding: 15px; margin-bottom: 20px; }
        .footer { padding: 15px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">New Contact Form Submission</h1>
        </div>
        <div class="content">';

if ($isUrgent) {
    $htmlBody .= '
            <div class="urgent">
                <strong>⚠️ ' . strtoupper($urgencyLabel) . '</strong>
            </div>';
}

$htmlBody .= '
            <div class="field">
                <div class="label">Name</div>
                <div class="value">' . htmlspecialchars($fullName) . '</div>
            </div>
            <div class="field">
                <div class="label">Email</div>
                <div class="value"><a href="mailto:' . htmlspecialchars($formData['email']) . '">' . htmlspecialchars($formData['email']) . '</a></div>
            </div>
            <div class="field">
                <div class="label">Phone</div>
                <div class="value"><a href="tel:' . preg_replace('/\D/', '', $formData['phone']) . '">' . htmlspecialchars($formData['phone']) . '</a></div>
            </div>';

if (!empty($formData['address'])) {
    $htmlBody .= '
            <div class="field">
                <div class="label">Property Address</div>
                <div class="value">' . htmlspecialchars($formData['address']) . '</div>
            </div>';
}

$htmlBody .= '
            <div class="field">
                <div class="label">Service Requested</div>
                <div class="value">' . htmlspecialchars($serviceLabel) . '</div>
            </div>
            <div class="field">
                <div class="label">Urgency</div>
                <div class="value">' . htmlspecialchars($urgencyLabel) . '</div>
            </div>
            <div class="field">
                <div class="label">Has Insurance</div>
                <div class="value">' . htmlspecialchars($formData['insurance']) . '</div>
            </div>';

if (!empty($formData['message'])) {
    $htmlBody .= '
            <div class="field">
                <div class="label">Message</div>
                <div class="value">' . nl2br(htmlspecialchars($formData['message'])) . '</div>
            </div>';
}

$htmlBody .= '
        </div>
        <div class="footer">
            Submitted on ' . date('F j, Y \a\t g:i A') . '<br>
            IP: ' . htmlspecialchars($formData['ip_address']) . '
        </div>
    </div>
</body>
</html>';

// Plain text version
$textBody = "NEW CONTACT FORM SUBMISSION\n";
$textBody .= "===========================\n\n";

if ($isUrgent) {
    $textBody .= "*** " . strtoupper($urgencyLabel) . " ***\n\n";
}

$textBody .= "Name: {$fullName}\n";
$textBody .= "Email: {$formData['email']}\n";
$textBody .= "Phone: {$formData['phone']}\n";

if (!empty($formData['address'])) {
    $textBody .= "Address: {$formData['address']}\n";
}

$textBody .= "Service: {$serviceLabel}\n";
$textBody .= "Urgency: {$urgencyLabel}\n";
$textBody .= "Has Insurance: {$formData['insurance']}\n";

if (!empty($formData['message'])) {
    $textBody .= "\nMessage:\n{$formData['message']}\n";
}

$textBody .= "\n---\nSubmitted: " . date('F j, Y \a\t g:i A');

// Send email
$emailSent = sendEmail(
    $config['to_email'],
    $subject,
    $htmlBody,
    $textBody,
    $formData['email'],
    $config['from_email'],
    $config['company_name']
);

// Send confirmation email to customer
$confirmSubject = "Thank you for contacting {$config['company_name']}";
$confirmHtml = '
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #1B4B8F; color: white; padding: 20px; text-align: center; }
        .content { padding: 30px; }
        .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; background: #f5f5f5; }
        .cta { display: inline-block; background: #1B4B8F; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">Clear Choice Restoration</h1>
        </div>
        <div class="content">
            <h2>Thank you, ' . htmlspecialchars($formData['first_name']) . '!</h2>
            <p>We have received your request for a <strong>' . htmlspecialchars($serviceLabel) . '</strong> and one of our roofing specialists will contact you within 24 hours.</p>
            <p>Here\'s a summary of your request:</p>
            <ul>
                <li><strong>Service:</strong> ' . htmlspecialchars($serviceLabel) . '</li>
                <li><strong>Urgency:</strong> ' . htmlspecialchars($urgencyLabel) . '</li>
            </ul>';

if ($isUrgent) {
    $confirmHtml .= '
            <p><strong>Since your request is marked as urgent, we will prioritize contacting you as soon as possible.</strong></p>';
}

$confirmHtml .= '
            <p>If you need immediate assistance, please call us:</p>
            <p style="font-size: 20px;"><strong>📞 (317) 358-8630</strong></p>
            <p>For emergencies: <strong>(317) 910-7605</strong> (24/7)</p>
            <p>Thank you for choosing Clear Choice Restoration!</p>
        </div>
        <div class="footer">
            <p>Clear Choice Restoration<br>
            195 N Shortridge Rd, Ste A<br>
            Indianapolis, IN 46219</p>
            <p>Family-owned and operated since 2001</p>
        </div>
    </div>
</body>
</html>';

$confirmText = "Thank you, {$formData['first_name']}!\n\n";
$confirmText .= "We have received your request for a {$serviceLabel} and one of our roofing specialists will contact you within 24 hours.\n\n";
$confirmText .= "If you need immediate assistance, please call us:\n";
$confirmText .= "Main: (317) 358-8630\n";
$confirmText .= "Emergency: (317) 910-7605 (24/7)\n\n";
$confirmText .= "Thank you for choosing Clear Choice Restoration!\n\n";
$confirmText .= "---\n";
$confirmText .= "Clear Choice Restoration\n";
$confirmText .= "195 N Shortridge Rd, Ste A\n";
$confirmText .= "Indianapolis, IN 46219";

// Send confirmation to customer
sendEmail(
    $formData['email'],
    $confirmSubject,
    $confirmHtml,
    $confirmText,
    $config['to_email'],
    $config['from_email'],
    $config['company_name']
);

// Return success response
echo json_encode([
    'success' => true,
    'message' => 'Thank you! Your message has been received. We will contact you within 24 hours.'
]);
