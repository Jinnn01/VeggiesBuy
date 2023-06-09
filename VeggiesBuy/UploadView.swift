//
//  UploadView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import VisionKit
import Foundation

struct VegetableUpload: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    let unit: String?
}

// add vegetable item
class AddItemModel: ObservableObject {
    @Published var vegetablesUpload: [VegetableUpload] = []
    
    func save(_ vegetable: VegetableUpload) {
        guard let url = URL(string: "http://localhost:5001/item") else {
            return
        }
        
        // Convert vegetable to JSON data
        guard let encodedData = try? JSONEncoder().encode(vegetable) else {
            print("Failed to encode item details")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = encodedData
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = URLSession.shared.dataTask(with: request) { _, _, error in
            if let error = error {
                print("Error: \(error)")
                return
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
    @State private var isShowingConfirmation = false
    @State private var isShowingAlert = false
    
    // Document scanning
    @State private var scannedImage: UIImage?
    @State private var isShowingScanner = false
    
    @State private var supermarkets: [String] = []
    @State private var selectedSupermarketName: String = ""
    
    init() {
        fetchSupermarkets()
        if let firstSupermarket = supermarkets.first {
            selectedSupermarketName = firstSupermarket
        }
    }
    
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
                                //TextField("Vegetable Price", text: formatCurrencyText($vegetablePrice))
                                    //.keyboardType(.decimalPad)
                                TextField("Vegetable Price", text: $vegetablePrice)
                                TextField("Vegetable Unit", text: $vegetableUnit)
                            }
                            
                            Section(header: Text("Supermarket Details"), footer: Text("You can either manually enter the item details with the form above, or tap the Camera icon in the top-left corner to open the OCR scanner.")) {
                                Picker("Supermaket:", selection: $selectedSupermarketName) {
                                    ForEach(supermarkets, id: \.self) { supermarket in
                                        Text(supermarket)
                                    }
                                }
                            }
                            var supermarkets: [String] {
                                get {
                                    fetchSupermarkets()
                                    return self.supermarkets
                                }
                                set {
                                    self.supermarkets = newValue
                                }
                            }
                        }
                    }
                    .background(Color(.systemBackground))


                    .sheet(isPresented: $isShowingScanner, onDismiss: {
                        
                    }) {
                        DocumentScannerView(scannedImage: $scannedImage)
                    }
                }
            }
            .navigationBarTitle("Upload")
            .toolbar {
                ToolbarItemGroup(placement: .navigationBarTrailing) {
                    Button(action: {
                        Task {
                            await saveVegItem()
                        }
                        
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
    /*
    func formatCurrencyText(_ text: Binding<String>) -> Binding<String> {
        return Binding<String>(
            get: { text.wrappedValue },
            set: { newValue in
                let filtered = newValue.filter { "0123456789.".contains($0) }
                text.wrappedValue = filtered.isEmpty ? "" : "$" + filtered
            }
        )
    }*/
    
    func fetchSupermarkets() {
        guard let url = URL(string: "http://localhost:5001/item") else {
            return
        }

        let task = URLSession.shared.dataTask(with: url) { data, _, error in
            if let error = error {
                print("Error: \(error)")
                return
            }

            if let data = data {
                do {
                    let vegetableUploads = try JSONDecoder().decode([VegetableUpload].self, from: data)
                    var uniqueSupermarkets: [String] = []
                    for vegetableUpload in vegetableUploads {
                        if !uniqueSupermarkets.contains(vegetableUpload.sname) {
                            uniqueSupermarkets.append(vegetableUpload.sname)
                        }
                    }
                    uniqueSupermarkets.sort()
                    DispatchQueue.main.async {
                        self.supermarkets = uniqueSupermarkets
                    }
                } catch {
                    print("Failed to decode vegetable uploads: \(error)")
                }
            }
        }
        task.resume()
    }

    
    func saveVegItem() async {
        if let price = Float(vegetablePrice) {
            let roundedPrice = (price * 100).rounded() / 100
            
            let vegetable = VegetableUpload(
                sname: selectedSupermarketName,
                vname: vegetableName,
                price: roundedPrice,
                unit: vegetableUnit
            )
            
            let addItemModel = AddItemModel()
            addItemModel.save(vegetable)
            
            isShowingAlert = true
        } else {
            print("Invalid price input")
        }
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
