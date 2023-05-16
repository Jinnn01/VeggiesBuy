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
    @Published var searchQuery: String = ""
    
    var filteredVegetables: [Vegetable] {
        if searchQuery.isEmpty {
            return vegetables
        } else {
            return vegetables.filter { vegetable in
                vegetable.vname.localizedCaseInsensitiveContains(searchQuery)
            }
        }
    }
    
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
    //@State private var searchQuery = ""
    
    var body: some View {
        NavigationView {
            VStack {
                
                List {
                    ForEach(viewModel.filteredVegetables, id: \.self) { vegetable in
                        VStack {
                            HStack {
                                Text(vegetable.vname.capitalized)
                                    .bold()
                                    .font(.system(size: 18))
                                Spacer()
                                Text("$\(vegetable.price, specifier: "%.2f")")
                            }
                            Text(vegetable.sname)
                                .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(3)
                        }
                        
                    }
                }
            }
            .searchable(text: $viewModel.searchQuery, prompt: "Search vegetables")
            .navigationBarTitle("Home")
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
