//
//  UploadView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import VisionKit

// add vegetable item
class AddItemModel: ObservableObject {
    @Published var vegetables: [Vegetable] = []
    
    func fetch() {
        //guard let url = URL(string: "https://iosacademy.io/api/v1/courses/index.php") else {
            //return
        guard let url = URL(string: "http://localhost:5006/item") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let vegetables = try JSONDecoder().decode([Vegetable].self, from: data)
                
                DispatchQueue.main.async {
                    self?.vegetables = vegetables
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}

struct DocumentScannerView: UIViewControllerRepresentable {
    typealias UIViewControllerType = VNDocumentCameraViewController
    
    @Binding var scannedImage: UIImage?
    @Environment(\.presentationMode) var presentationMode
    
    func makeUIViewController(context: Context) -> VNDocumentCameraViewController {
        let documentScannerViewController = VNDocumentCameraViewController()
        documentScannerViewController.delegate = context.coordinator
        return documentScannerViewController
    }
    
    func updateUIViewController(_ uiViewController: VNDocumentCameraViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, VNDocumentCameraViewControllerDelegate {
        let parent: DocumentScannerView
        
        init(_ parent: DocumentScannerView) {
            self.parent = parent
        }
        
        func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFinishWith scan: VNDocumentCameraScan) {
            guard scan.pageCount >= 1 else {
                controller.dismiss(animated: true) {
                    self.parent.presentationMode.wrappedValue.dismiss()
                }
                return
            }
            
            let image = scan.imageOfPage(at: 0)
            parent.scannedImage = image
            
            controller.dismiss(animated: true) {
                self.parent.presentationMode.wrappedValue.dismiss()
            }
        }
        
        func documentCameraViewControllerDidCancel(_ controller: VNDocumentCameraViewController) {
            controller.dismiss(animated: true) {
                self.parent.presentationMode.wrappedValue.dismiss()
            }
        }
        
        func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFailWithError error: Error) {
            print("Document scanning failed with error: \(error)")
            
            controller.dismiss(animated: true) {
                self.parent.presentationMode.wrappedValue.dismiss()
            }
        }
    }
}


struct UploadView: View {
    
    @State private var vegetableName = ""
    @State private var vegetablePrice = ""
    @State private var vegetableUnit = ""
    @State private var supermarketName = ""
    @State private var isShowingAlert = false
    
    // Document scanning
    @State private var scannedImage: UIImage?
    @State private var isShowingScanner = false
    
    var body: some View {
        NavigationView {
            ZStack {
                if let image = scannedImage {
                    Image(uiImage: image)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                } else {
                    
                    VStack {
                        Form {
                            Section(header: Text("Vegetable Details")) {
                                TextField("Vegetable Name", text: $vegetableName)
                                TextField("Vegetable Price", text: $vegetablePrice)
                                TextField("Vegetable Unit", text: $vegetableUnit)
                            }
                            
                            Section(header: Text("Supermarket Details"), footer: Text("You can either manually enter the item details with the form above, or tap the Camera icon in the top-left corner to open the OCR scanner.")) {
                                TextField("Supermarket Name", text: $supermarketName)
                            }
                        }
                        //.padding(.top, 10)
                        /*
                        Text("You can either manually enter the item details with the form above, or tap the Camera icon in the top-left corner to open the OCR scanner.\n\nThe OCR feature will read your supermarket receipt, fetching the item and price details which you can verify before submitting.")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .padding(.horizontal, 20)*/
                    }
                    .background(Color(.systemBackground))


                    .sheet(isPresented: $isShowingScanner, onDismiss: {
                        // Handle dismiss action if needed
                    }) {
                        DocumentScannerView(scannedImage: $scannedImage)
                    }
                }
            }
            .navigationBarTitle("Upload")
            .toolbar {
                ToolbarItemGroup(placement: .navigationBarTrailing) {
                    Button(action: {
                        saveVegItem()
                    }) {
                        Text("Submit")
                            .font(.headline)
                    }
                }
                ToolbarItemGroup(placement: .navigationBarLeading) {
                    Button(action: {
                        isShowingScanner = true
                    }) {
                        Image(systemName: "camera.fill")
                            .imageScale(.large)
                    }
                }
            }
        }
        .alert(isPresented: $isShowingAlert) {
            Alert(title: Text("Success"), message: Text("Vegetable successfully submitted!"), dismissButton: .default(Text("OK")))
        }
    }
    
    func saveVegItem() {
        isShowingAlert = true
        print("Vegetable item submitted!")
    }
}


struct UploadView_Previews: PreviewProvider {
    static var previews: some View {
        UploadView()
    }
}

// disable the keyboard when not in use
#if canImport(UIKit)
extension View {
    func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}
#endif
