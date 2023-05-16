//
//  MapView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import MapKit



extension UIColor {
    convenience init(hex: String) {
        let scanner = Scanner(string: hex)
        scanner.currentIndex = hex.index(hex.startIndex, offsetBy: 1) // Skip the # character
        var rgbValue: UInt64 = 0
        scanner.scanHexInt64(&rgbValue)
        
        let red = CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0
        let green = CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0
        let blue = CGFloat(rgbValue & 0x0000FF) / 255.0
        
        self.init(red: red, green: green, blue: blue, alpha: 1.0)
    }
}

struct VegetableMap: Hashable, Codable, Identifiable {
    let id = UUID()
    let sname: String
    let vname: String
    let price: Float
    //let unit: String
    let slatitude: String
    let slongitude: String
    //let image: String
}

/*
struct Supermarket: Hashable, Codable, Identifiable {
    let id = UUID()
    let sname: String
    let slatitude: String
    let slongitude: String
    let saddress: String
}*/

class ViewMapModel: ObservableObject {
    @Published var vegetablesMap: [VegetableMap] = []
    
    func fetch() {
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
                let vegetablesMap = try JSONDecoder().decode([VegetableMap].self, from: data)
                DispatchQueue.main.async {
                    self?.vegetablesMap = vegetablesMap
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}

struct MapView: View {
    @StateObject var viewModelMap = ViewMapModel()
    @State private var searchQuery = ""
    @State private var selectedAnnotation: VegetableMap? = nil
    @State private var mapRegion = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: -34.4110, longitude: 150.8948), span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05))
    @State private var isShowingAlert = false
    @State private var isShowingModal = false
    @Environment(\.colorScheme) var colorScheme
    
    var filteredVegetablesMap: [VegetableMap] {
        if searchQuery.isEmpty {
            return viewModelMap.vegetablesMap
        } else {
            return viewModelMap.vegetablesMap.filter { vegetableMap in
                vegetableMap.sname.localizedCaseInsensitiveContains(searchQuery)
            }
        }
    }
    
    var firstFilteredVegetableMap: VegetableMap? {
        filteredVegetablesMap.first
    }
    
    var body: some View {
        NavigationView {
            ZStack {
                Map(coordinateRegion: $mapRegion, annotationItems: filteredVegetablesMap) { vegetableMap in
                    MapAnnotation(coordinate: CLLocationCoordinate2D(latitude: Double(vegetableMap.slatitude) ?? 0.0, longitude: Double(vegetableMap.slongitude) ?? 0.0)) {
                        VStack {
                            Image(systemName: "mappin")
                                .resizable()
                                .frame(width: 10, height: 32)
                                .foregroundColor(.red)
                            ZStack {
                                
                                Rectangle()
                                    .foregroundColor(.blue)
                                Text(vegetableMap.vname)
                                    //.foregroundColor(.primary)
                                    .bold()
                                    .foregroundColor(.white)
                                    .font(.system(size: 14))
                                    //.lineLimit(1)
                                    //.truncationMode(.tail)
                            }
                            
                        }
                        .onTapGesture {
                            selectedAnnotation = vegetableMap
                            isShowingAlert = true
                        }
                    }
                }
                VStack {
                    TextField("Search vegetables", text: $searchQuery)
                        .padding()
                        .background(colorScheme == .dark ? Color.black : Color.white)
                        .foregroundColor(colorScheme == .dark ? Color.white : Color.black)
                        .cornerRadius(8)
                        .padding(.horizontal)
                        .offset(y: 60)
                        .shadow(radius: 4)
                        //.accentColor(.white)
                        //.background(Color(UIColor.systemBackground))
                    Spacer()
                }
                
            }
            //.searchable(text: $searchQuery, prompt: "Search")
            .edgesIgnoringSafeArea(.top)
            .alert(isPresented: $isShowingAlert) {
                guard let selectedAnnotation = selectedAnnotation else {
                    return Alert(title: Text("Error"), message: Text("An error occurred."), dismissButton: .default(Text("OK")))
                }
                
                return Alert(
                    title: Text(selectedAnnotation.vname.capitalized),
                    message:
                        Text(selectedAnnotation.sname +
                             "\nPrice: " + String(format: "$%.2f", selectedAnnotation.price)),
                    primaryButton: .default(Text("Report Mismatch").foregroundColor(.red)),
                    secondaryButton: .default(Text("Back to Map"), action: {
                        // Perform action to go to Home view
                    })
                )
            }
            .onAppear {
                viewModelMap.fetch()
            }
        }
    }
    
    struct ModalView: View {
        let selectedAnnotation: VegetableMap
        @Binding var isShowingModal: Bool

        var body: some View {
            VStack {
                Text(selectedAnnotation.sname)
                Text(selectedAnnotation.slatitude)

                Button("Report Mismatch") {
                    // Perform action for reporting mismatch
                }
                .padding()

                Button("Back to Map") {
                    isShowingModal = false
                }
                .padding()
            }
        }
    }
    
    struct MapView_Previews: PreviewProvider {
        static var previews: some View {
            MapView()
        }
    }
}
