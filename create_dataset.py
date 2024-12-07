import os
import pandas as pd

def load_emails_from_folder(folder_path, label):
    """
    Loads all emails from the specified folder and assigns the given label.
    
    Args:
        folder_path (str): Path to the folder containing email text files.
        label (int): Label for the emails (0 for legitimate, 1 for spam).
    
    Returns:
        tuple: Two lists containing emails and their corresponding labels.
    """
    emails = []
    labels = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                    emails.append(content)
                    labels.append(label)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
    return emails, labels

def create_csv(enron_spam_folder, output_csv):
    """
    Iterates through all enronN directories within enron_spam_folder,
    loads emails from ham and spam subfolders, and compiles them into a CSV.
    
    Args:
        enron_spam_folder (str): Path to the 'enron_spam' directory.
        output_csv (str): Path for the output CSV file.
    """
    all_emails = []
    all_labels = []
    
    # Iterate over all enronN directories (e.g., enron1, enron2, ...)
    for enron_dir in os.listdir(enron_spam_folder):
        enron_path = os.path.join(enron_spam_folder, enron_dir)
        if os.path.isdir(enron_path):
            ham_folder = os.path.join(enron_path, 'ham')
            spam_folder = os.path.join(enron_path, 'spam')
            
            # Load ham emails
            if os.path.exists(ham_folder):
                ham_emails, ham_labels = load_emails_from_folder(ham_folder, 0)  # 0 for legitimate
                all_emails.extend(ham_emails)
                all_labels.extend(ham_labels)
                print(f"Loaded {len(ham_emails)} legitimate emails from {ham_folder}")
            else:
                print(f"Warning: 'ham' folder not found in {enron_path}")
                
            # Load spam emails
            if os.path.exists(spam_folder):
                spam_emails, spam_labels = load_emails_from_folder(spam_folder, 1)  # 1 for spam
                all_emails.extend(spam_emails)
                all_labels.extend(spam_labels)
                print(f"Loaded {len(spam_emails)} spam emails from {spam_folder}")
            else:
                print(f"Warning: 'spam' folder not found in {enron_path}")
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame({
        'email': all_emails,
        'label': all_labels
    })
    
    df.to_csv(output_csv, index=False)
    print(f"CSV file created at {output_csv} with {len(df)} total emails.")

if __name__ == "__main__":
    # Define paths
    enron_spam_folder = 'enron-spam'  # Updated to match the actual directory name
    output_csv = 'emails_dataset.csv'
    
    # Check if enron_spam_folder exists
    if not os.path.exists(enron_spam_folder):
        print(f"Error: The folder '{enron_spam_folder}' does not exist in the current directory.")
        print("Please ensure that the Enron Spam dataset is correctly downloaded and extracted.")
        exit(1)
    
    # Create the CSV
    create_csv(enron_spam_folder, output_csv)
