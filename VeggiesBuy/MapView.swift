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
    let unit: String?
    let slatitude: String
    let slongitude: String
}

func getTextWidth(_ text: String) -> CGFloat {
    let font = UIFont.systemFont(ofSize: 14, weight: .bold)
    let attributes = [NSAttributedString.Key.font: font]
    let size = (text as NSString).size(withAttributes: attributes)
    return ceil(size.width) + 12
}

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
                vegetableMap.vname.localizedCaseInsensitiveContains(searchQuery)
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
                        if searchQuery.isEmpty {
                            // Custom annotation for sname
                            ZStack {
                                Rectangle()
                                    .foregroundColor(Color(UIColor(hex: "#19AA5C")))
                                    .frame(width: getTextWidth(vegetableMap.sname.components(separatedBy: " ").first ?? ""), height: 24)
                                    .cornerRadius(8)
                                Text(vegetableMap.sname.components(separatedBy: " ").first ?? "")
                                    .foregroundColor(.white)
                                    .font(.system(size: 14, weight: .bold))
                            }
                        } else {
                            VStack {
                                ZStack {
                                    Rectangle()
                                        .foregroundColor(Color(UIColor(hex: "#DA7843")))
                                        .frame(width: 60, height: 24)
                                        .cornerRadius(8)
                                    Text("$\(String(format: "%.2f", vegetableMap.price))")
                                        .foregroundColor(.white)
                                        .font(.system(size: 14, weight: .bold))
                                }
                            }
                            .onTapGesture {
                                selectedAnnotation = vegetableMap
                                isShowingAlert = true
                            }
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
                    Spacer()
                }
                
            }
            .edgesIgnoringSafeArea(.top)
            .alert(isPresented: $isShowingAlert) {
                guard let selectedAnnotation = selectedAnnotation else {
                    return Alert(title: Text("Error"), message: Text("An error occurred."), dismissButton: .default(Text("OK")))
                }
                
                return Alert(
                    title: Text(selectedAnnotation.vname.capitalized),
                    message: {
                        if selectedAnnotation.unit != nil {
                            return Text(selectedAnnotation.sname + "\n")
                                + Text("$\(selectedAnnotation.price, specifier: "%.2f")/\(selectedAnnotation.unit!)")
                        } else {
                            return Text(selectedAnnotation.sname + "\n")
                                + Text("$\(selectedAnnotation.price, specifier: "%.2f")")
                        }
                    }(),
                    primaryButton: .destructive(Text("Report Mismatch")),
                    secondaryButton: .default(Text("Back to Map"), action: {
                        
                    })
                )
            }
            .onAppear {
                viewModelMap.fetch()
            }
        }
    }

    struct MapView_Previews: PreviewProvider {
        static var previews: some View {
            MapView()
        }
    }
}
