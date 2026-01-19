<?php
/**
 * Staff Management API
 * Clear Choice Restoration
 *
 * Handles CRUD operations for staff members
 * Data stored in ../data/staff.json
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Data file path
$dataFile = __DIR__ . '/../data/staff.json';

// Ensure data directory exists
$dataDir = dirname($dataFile);
if (!is_dir($dataDir)) {
    mkdir($dataDir, 0755, true);
}

// Initialize data file if it doesn't exist
if (!file_exists($dataFile)) {
    file_put_contents($dataFile, json_encode(['staff' => []], JSON_PRETTY_PRINT));
}

/**
 * Load staff data from JSON file
 */
function loadStaffData($file) {
    $content = file_get_contents($file);
    $data = json_decode($content, true);
    return $data ?: ['staff' => []];
}

/**
 * Save staff data to JSON file
 */
function saveStaffData($file, $data) {
    return file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}

/**
 * Sanitize input data
 */
function sanitizeInput($input) {
    if (is_array($input)) {
        return array_map('sanitizeInput', $input);
    }
    return htmlspecialchars(strip_tags(trim($input)), ENT_QUOTES, 'UTF-8');
}

/**
 * Validate staff data
 */
function validateStaff($staff) {
    $errors = [];

    if (empty($staff['name'])) {
        $errors[] = 'Name is required';
    }

    if (empty($staff['role'])) {
        $errors[] = 'Role is required';
    }

    if (!empty($staff['email']) && !filter_var($staff['email'], FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Invalid email format';
    }

    if (!empty($staff['photo']) && !filter_var($staff['photo'], FILTER_VALIDATE_URL)) {
        $errors[] = 'Invalid photo URL';
    }

    return $errors;
}

// Handle GET requests
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = $_GET['action'] ?? 'list';

    switch ($action) {
        case 'list':
            $data = loadStaffData($dataFile);
            echo json_encode($data);
            break;

        case 'get':
            $id = $_GET['id'] ?? '';
            $data = loadStaffData($dataFile);
            $staff = null;

            foreach ($data['staff'] as $s) {
                if ($s['id'] === $id) {
                    $staff = $s;
                    break;
                }
            }

            if ($staff) {
                echo json_encode(['success' => true, 'staff' => $staff]);
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'error' => 'Staff member not found']);
            }
            break;

        default:
            http_response_code(400);
            echo json_encode(['success' => false, 'error' => 'Invalid action']);
    }
    exit();
}

// Handle POST requests
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);

    if (!$input) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Invalid JSON input']);
        exit();
    }

    $action = $input['action'] ?? '';

    switch ($action) {
        case 'create':
            $staffInput = sanitizeInput($input['staff'] ?? []);
            $errors = validateStaff($staffInput);

            if (!empty($errors)) {
                http_response_code(400);
                echo json_encode(['success' => false, 'errors' => $errors]);
                exit();
            }

            $data = loadStaffData($dataFile);

            $newStaff = [
                'id' => $staffInput['id'] ?? 'staff_' . time() . '_' . bin2hex(random_bytes(4)),
                'name' => $staffInput['name'],
                'role' => $staffInput['role'],
                'bio' => $staffInput['bio'] ?? '',
                'photo' => $staffInput['photo'] ?? '',
                'email' => $staffInput['email'] ?? '',
                'phone' => $staffInput['phone'] ?? '',
                'created_at' => date('Y-m-d H:i:s')
            ];

            $data['staff'][] = $newStaff;
            saveStaffData($dataFile, $data);

            echo json_encode(['success' => true, 'staff' => $newStaff, 'message' => 'Staff member created']);
            break;

        case 'update':
            $staffInput = sanitizeInput($input['staff'] ?? []);
            $id = $staffInput['id'] ?? '';

            if (empty($id)) {
                http_response_code(400);
                echo json_encode(['success' => false, 'error' => 'Staff ID is required']);
                exit();
            }

            $errors = validateStaff($staffInput);
            if (!empty($errors)) {
                http_response_code(400);
                echo json_encode(['success' => false, 'errors' => $errors]);
                exit();
            }

            $data = loadStaffData($dataFile);
            $found = false;

            foreach ($data['staff'] as $index => $s) {
                if ($s['id'] === $id) {
                    $data['staff'][$index] = [
                        'id' => $id,
                        'name' => $staffInput['name'],
                        'role' => $staffInput['role'],
                        'bio' => $staffInput['bio'] ?? '',
                        'photo' => $staffInput['photo'] ?? '',
                        'email' => $staffInput['email'] ?? '',
                        'phone' => $staffInput['phone'] ?? '',
                        'created_at' => $s['created_at'] ?? date('Y-m-d H:i:s'),
                        'updated_at' => date('Y-m-d H:i:s')
                    ];
                    $found = true;
                    break;
                }
            }

            if (!$found) {
                http_response_code(404);
                echo json_encode(['success' => false, 'error' => 'Staff member not found']);
                exit();
            }

            saveStaffData($dataFile, $data);
            echo json_encode(['success' => true, 'message' => 'Staff member updated']);
            break;

        case 'delete':
            $id = $input['id'] ?? '';

            if (empty($id)) {
                http_response_code(400);
                echo json_encode(['success' => false, 'error' => 'Staff ID is required']);
                exit();
            }

            $data = loadStaffData($dataFile);
            $initialCount = count($data['staff']);
            $data['staff'] = array_values(array_filter($data['staff'], function($s) use ($id) {
                return $s['id'] !== $id;
            }));

            if (count($data['staff']) === $initialCount) {
                http_response_code(404);
                echo json_encode(['success' => false, 'error' => 'Staff member not found']);
                exit();
            }

            saveStaffData($dataFile, $data);
            echo json_encode(['success' => true, 'message' => 'Staff member deleted']);
            break;

        case 'reorder':
            $order = $input['order'] ?? [];

            if (empty($order) || !is_array($order)) {
                http_response_code(400);
                echo json_encode(['success' => false, 'error' => 'Order array is required']);
                exit();
            }

            $data = loadStaffData($dataFile);
            $staffById = [];

            foreach ($data['staff'] as $s) {
                $staffById[$s['id']] = $s;
            }

            $reordered = [];
            foreach ($order as $id) {
                if (isset($staffById[$id])) {
                    $reordered[] = $staffById[$id];
                    unset($staffById[$id]);
                }
            }

            // Add any remaining staff (in case of data mismatch)
            foreach ($staffById as $s) {
                $reordered[] = $s;
            }

            $data['staff'] = $reordered;
            saveStaffData($dataFile, $data);

            echo json_encode(['success' => true, 'message' => 'Staff order updated']);
            break;

        default:
            http_response_code(400);
            echo json_encode(['success' => false, 'error' => 'Invalid action']);
    }
    exit();
}

// Handle other methods
http_response_code(405);
echo json_encode(['success' => false, 'error' => 'Method not allowed']);
