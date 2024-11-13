#### fzvis v0.2.1 Tutorial:
## Prerequisites

1.  libpressio
2.  npm (for frontend)
3.  Python 3 (for backend)
4.  VM Image: Use the VM image - fzvis-v0.2.1
5.  SSH Access: Connect to the VM using your floating IP
6.  Then Follow the instructions to setup and run the project

### To run the project:
## 1. Initialize the Environment
Run the setup script to load libpressio, Node, and set up the Python environment:
```
source setup.sh
```
## 2. Set the Floating IP for Frontend-Backend Communication
To ensure the frontend connects properly to the backend, you’ll need to set the floating IP in the DataSelection.vue file. Follow these steps:
1.  Find the Floating IP of your Chameleon VM
2.  Open DataSelection.vue located in your project’s src/components directory
3.  Replace the Floating IP:
    Locate the line where the WebSocket or HTTP URL is specified. It will look something like this:
    ```
    const wsURL = `${wsProtocol}//<your-floating-ip>:8080/ws`;
    ```
4.  Replace <your-floating-ip> with the actual IP of your instance
    For example:
    ```
    const wsURL = `${wsProtocol}//192.5.86.216:8080/ws`;
    ```
5.  Save the File and re-run your application as usual


## 3. Run the Frontend and Backend
Start both the backend and frontend concurrently:
```
concurrently "python3 src/components/main.py" "npm run serve"
```

### Project Repository
```
git clone https://github.com/YuxiaoLi1234/fzvis.git
```
## Dashboard Overview - 
The dashboard allows for easy navigation and interaction with compressor configurations, dataset uploads, and metric visualizations.

The dashboard should look like this figure-
<img width="1450" alt="Screenshot 2024-10-15 at 7 33 09 PM" src="https://github.com/user-attachments/assets/4ceef310-2008-403f-88a4-1f332e88943f">

### Workflow

## Running a Compressor:
- Compressor Selection: Choose a compressor from the dropdown list (e.g., SZ, ZFP).
- Error Bound: Enter the error bound value.
- Metric Categories: Select the categories of metrics you want to visualize.
- Configuration: Save and confirm your configurations.
  
<img width="1446" alt="Screenshot 2024-10-15 at 7 29 53 PM" src="https://github.com/user-attachments/assets/7ac7f072-bc1b-4a9f-9af5-ceef5bd8fc85">

## Input Dataset
- Upload the Input Dataset: Upload your dataset file and fill in the dataset dimensions along with the precision value.
- Run the Compressors: Submit the configurations and execute the compression.
  
<img width="416" alt="Screenshot 2024-10-15 at 7 30 59 PM" src="https://github.com/user-attachments/assets/72c360aa-9ae1-4a3c-b383-e1a8fcff0838">

## Visualization
The result in the visualization module should appear as shown below:

<img width="1027" alt="Screenshot 2024-10-15 at 7 31 33 PM" src="https://github.com/user-attachments/assets/06dda073-6252-4d4c-8beb-5061a40bbb28">

### Interaction usage:
## Compare Matrics among Compressors.
1. After running all compressors, you need to click on the name of the compressors you want to compare:
   
<img width="1027" alt="Screenshot 2024-10-15 at 7 31 33 PM" src="https://github.com/user-attachments/assets/06dda073-6252-4d4c-8beb-5061a40bbb28">

2. Click on the compressor_compare button, the result shoule be like the figure below:
   
<img width="1027" alt="Screenshot 2024-10-15 at 7 32 08 PM" src="https://github.com/user-attachments/assets/5d408cd1-7e82-49e4-a7fc-78ff3bfd89eb">

(click on the all_compressor button to return to the visualization of barcharts of all of the compressors)

## Slice Visualization:
After running the compressors, visualize a slice of your input data.

- Input the slice_id.
- Click the DataVis button to view the data.
- Use the colormap selector to customize your view.
- Add control points (add_points mode) or drag existing control points (use current control points mode).
  
<img width="420" alt="Screenshot 2024-10-15 at 7 32 43 PM" src="https://github.com/user-attachments/assets/66be4982-2995-4e48-b7a8-cbf3744d65a2">
