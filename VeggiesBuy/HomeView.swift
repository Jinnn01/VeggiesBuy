//
//  HomeView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI


// iosacademy tutorial
/*
struct Store: Hashable, Codable {
    let sname: String
    //let image: String
}*/

struct Vegetable: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    //let unit: String
    //let image: String
}
/*
struct Store: Hashable, Codable {
    let sname: String
    let saddress: String
    let slatitude: String
    let slongitude: String
    //let vname: String
    //let price: Float
    //let unit: String
    //let image: String
}*/

// fetch store names
class ViewModel: ObservableObject {
    @Published var vegetables: [Vegetable] = []
    
    //http://localhost:5000/api/items
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

struct HomeView: View {
    @StateObject var viewModel = ViewModel()
    @State private var searchText = ""
    
    var body: some View {
        NavigationView {
            VStack {
                
                List {
                    ForEach(viewModel.vegetables, id: \.self) { vegetable in
                        HStack {
                            Text(vegetable.vname)
                                .bold()
                            Spacer()
                            Text("$\(vegetable.price, specifier: "%.2f")")
                        }
                        .padding(3)
                    }
                }
            }
            .searchable(text: $searchText, prompt: "Search")
            .navigationBarTitle("Home")
            // from the iosacademy tutorial
            
            .onAppear {
                viewModel.fetch()
            }
        }
    }
    
    /*
    var filteredItems: [String] {
        if searchText.isEmpty {
            return allProducts
        } else {
            return allProducts.filter { $0.localizedCaseInsensitiveContains(searchText)}
        }
    }*/

}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
